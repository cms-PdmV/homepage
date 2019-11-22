import sys
import json
import time
import os
# sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM


mcm = McM(dev=False, debug=True, cookie=os.getenv('PROD_COOKIE'))
pmp = McM(dev=False, debug=True, cookie=os.getenv('PROD_COOKIE'))
pmp.server = pmp.server.replace('mcm', 'pmp')


def get_list_of_campaigns():
    campaigns = mcm.get('campaigns', query='prepid=*MiniAOD*&status=started')
    print('%s MiniAOD started campaigns' % (len(campaigns)))
    campaigns_with_submitted_requests = []
    for campaign in campaigns:
        campaign_prepid = campaign['prepid']
        requests = mcm.get('requests', query='member_of_campaign=%s&status=submitted' % (campaign_prepid), page=0)
        if len(requests) > 0:
            campaigns_with_submitted_requests.append(campaign_prepid)
        else:
            print('Campaign %s does not have any submitted requests' % (campaign_prepid))

    rereco_campaigns = pmp._McM__get('api/objects?r=rereco_campaigns')
    rereco_campaigns = [x for x in rereco_campaigns if 'nanoaod' not in x.lower()]
    campaigns_with_submitted_requests.extend(rereco_campaigns)
    return campaigns_with_submitted_requests


def aggregate_data_points(data, timestamps):
    """
    Given list of event dictionaries (time, done, produced, invalid, expected)
    and timestamps aggregate everything into nice objects at given times
    """
    points = []
    for timestamp in timestamps:
        point = {'done': 0, 'produced': 0, 'expected': 0, 'invalid': 0, 'time': timestamp}
        for key in data:
            for details in reversed(data[key]):
                if details['time'] <= timestamp:
                    point['done'] += details['done']
                    point['invalid'] += details['invalid']
                    point['produced'] += details['produced']
                    point['expected'] += details['expected']
                    break

        point['events'] = point['invalid'] + point['produced'] + point['done']
        point['change'] = 0
        if len(points) > 0:
            last_point = points[-1]
            point['change'] = point['events'] - last_point['events']

        points.append(point)

    return points


granularity = 500
priority_blocks = {
    'block1': '110000,',
    'block2': '90000,109999',
    'block3': '85000,89999',
    'block4': '80000,84999',
    'block5': '70000,79999',
    'block6': ',69999',
}
campaigns = {}
campaign_list = get_list_of_campaigns()

for i, campaign in enumerate(campaign_list):
    print('Getting %s from pMp, %s/%s' % (campaign, i + 1, len(campaign_list)))
    campaigns[campaign] = {}
    campaign_results = pmp._McM__get('api/historical?r=%s&granularity=20' % (campaign))
    if len(campaign_results['results']['submitted_requests']) == 0:
        print('Skipping %s because no submitted requests' % (campaign))
        continue

    pwgs = campaign_results['results']['pwg'].keys()
    print('Got %s pwgs for %s' % (len(pwgs), campaign))
    for pwg in pwgs:
        campaigns[campaign][pwg] = {}
        for block_name, priority in priority_blocks.items():
            print('Getting plot for %s %s %s' % (campaign, pwg, block_name))
            campaigns[campaign][pwg][block_name] = pmp._McM__get('api/historical?r=%s&granularity=%s&priority=%s&pwg=%s' % (campaign,
                                                                                                                            granularity,
                                                                                                                            priority,
                                                                                                                            pwg))['results']['data']

print('Got %s campaigns' % (len(campaigns)))
now = int(time.time())
step = 3600 * 8 # 8 hours
past = now - 3600 * 24 * 7 - step
timestamps = list(range(past * 1000, now * 1000, step * 1000))
# if timestamps[-1] != now:
#     timestamps[-1] = now * 1000
timestamps.append(now * 1000)

print('Timestamps up to now %s' % (', '.join([str(x) for x in timestamps])))

# Split all campaigns into nice equal timestamps
changes = {}
used_pwgs = set()
used_blocks = set()
for campaign_name in campaigns:
    for pwg in campaigns[campaign_name]:
        for block_name in campaigns[campaign_name][pwg]:
            block = aggregate_data_points({campaign_name: campaigns[campaign_name][pwg][block_name]}, timestamps)
            block = [x['change'] for x in block]
            block = block[1:]
            block_sum = sum(block)
            if block_sum > 0:
                if campaign_name not in changes:
                    changes[campaign_name] = {}

                if pwg not in changes[campaign_name]:
                    changes[campaign_name][pwg] = {}

                changes[campaign_name][pwg][block_name] = block
                used_pwgs.add(pwg)
                used_blocks.add(block_name)


changes = {'timestamps': timestamps,
           'data': changes,
           'pwgs': sorted(list(used_pwgs)),
           'blocks': sorted(list(used_blocks))}

# print(json.dumps(changes, indent=4))
if len(changes) > 0:
    f = open('file.json', 'w')
    json.dump(changes, f)
else:
    print('No results?')
