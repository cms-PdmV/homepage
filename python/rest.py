import sys
import os
import json
try:
    import httplib
except:
    from http.client import HTTPSConnection

try:
    import cookielib
except:
    import http.cookiejar as cookielib

try:
    import urllib2 as urllib
except:
    import urllib.request as urllib
    
import traceback
import logging


class HTTPSClientAuthHandler(urllib.HTTPSHandler):
    def __init__(self, key, cert):
        urllib.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


class MethodRequest(urllib.Request):
    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        if self._method is not None:
            return self._method
        return urllib.Request.get_method(self, *args, **kwargs)


class McM:
    def __init__(self, id='sso', debug=False, cookie=None, dev=True, int=False):
        self.dev = dev
        if self.dev:
            self.host = 'cms-pdmv-dev.cern.ch'
        elif int:
            self.host = 'cms-pdmv-int.cern.ch'
        else:
            self.host = 'cms-pdmv.cern.ch'

        self.server = 'https://' + self.host + '/mcm/'
        self.id = id
        # Set up logging
        if debug:
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO

        logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging_level)
        # Create openers
        self.__connect(cookie)

    def __connect(self, cookie=None):
        if self.id == 'cert':
            self.opener = urllib.build_opener(HTTPSClientAuthHandler(self.host,
                                                                     os.getenv('X509_USER_PROXY'),
                                                                     os.getenv('X509_USER_PROXY')))
        elif self.id == 'sso':
            if cookie:
                self.cookie_filename = cookie
            else:
                if self.dev:
                    self.cookie_filename = '%s/private/dev-cookie.txt' % (os.getenv('HOME'))
                else:
                    self.cookie_filename = '%s/private/prod-cookie.txt' % (os.getenv('HOME'))

            if not os.path.isfile(self.cookie_filename):
                logging.warning('The required sso cookie file is absent. Trying to make one for you')
                os.system('cern-get-sso-cookie -u %s -o %s --reprocess --krb' % (self.server,
                                                                     self.cookie_filename))

                if not os.path.isfile(self.cookie_filename):
                    logging.error('Unfortunately sso cookie file cannot be made automatically. Quitting...')
                    sys.exit(1)
            else:
                logging.info('Found a cookie file at %s. Make sure it\'s not expired!' % (self.cookie_filename))

            cookie_jar = cookielib.MozillaCookieJar(self.cookie_filename)
            cookie_jar.load()
            for c in cookie_jar:
                logging.debug('Cookie %s', c)

            self.opener = urllib.build_opener(urllib.HTTPCookieProcessor(cookie_jar))
        else:
            self.opener = urllib.build_opener()

    # Generic methods for GET, PUT, DELETE HTTP methods
    def __get(self, url, parse_json=True):
        url = self.server + url
        headers = {'User-Agent': 'McM Scripting'}
        request = MethodRequest(url, headers=headers, method='GET')
        logging.debug('GET %s', url)
        try:
            response = self.opener.open(request)
            response = response.read()
            response = response.decode('utf-8')
            logging.debug('Received a response to %s. Length %s', url, len(response))
            if parse_json:
                return json.loads(response)
            else:
                return response
        except Exception as ex:
            logging.error('Error while making a GET request to %s.\nException: %s.\nTraceback: %s', url, ex, traceback.format_exc())
            return None

    def __put(self, url, data, parse_json=True):
        url = self.server + url
        put_data = json.dumps(data)
        headers = {'User-Agent': 'McM Scripting', 'Content-Type': 'application/json'}
        request = MethodRequest(url, data=put_data, headers=headers, method='PUT')
        logging.debug('PUT %s. Data %s', url, put_data)
        try:
            response = self.opener.open(request)
            response = response.read()
            response = response.decode('utf-8')
            logging.debug('Received a response to %s. Length %s', url, len(response))
            if parse_json:
                return json.loads(response)
            else:
                return response
        except Exception as ex:
            logging.error('Error while making a GET request to %s.\nException: %s.\nTraceback: %s', url, ex, traceback.format_exc())
            return None

    def __post(self, url, data, parse_json=True):
        url = self.server + url
        post_data = json.dumps(data)
        headers = {'User-Agent': 'McM Scripting', 'Content-Type': 'application/json'}
        request = MethodRequest(url, data=post_data, headers=headers, method='POST')
        logging.debug('POST %s. Data %s', url, post_data)
        try:
            response = self.opener.open(request)
            response = response.read()
            response = response.decode('utf-8')
            logging.debug('Received a response to %s. Length %s', url, len(response))
            if parse_json:
                return json.loads(response)
            else:
                return response
        except Exception as ex:
            logging.error('Error while making a GET request to %s.\nException: %s.\nTraceback: %s', url, ex, traceback.format_exc())
            return None

    def __delete(self, url):
        url = self.server + url
        headers = {'User-Agent': 'McM Scripting'}
        request = MethodRequest(url, headers=headers, method='DELETE')
        logging.debug('DELETE %s', url)
        try:
            response = self.opener.open(request)
            response = response.read()
            response = response.decode('utf-8')
            logging.debug('Received a response to %s. Length %s', url, len(response))
            if parse_json:
                return json.loads(response)
            else:
                return response
        except Exception as ex:
            logging.error('Error while making a GET request to %s.\nException: %s.\nTraceback: %s', url, ex, traceback.format_exc())
            return None

    # McM methods
    def get(self, object_type, object_id=None, query='', method='get', page=-1):
        """
        Get data from McM
        object_type - [chained_campaigns, chained_requests, campaigns, requests, flows, etc.]
        object_id - usually prep id of desired object
        query - query to be run in order to receive an object, e.g. tags=M17p1A, multiple parameters can be used with & tags=M17p1A&pwg=HIG
        method - action to be performed, such as get, migrate or inspect
        page - which page to be fetched. -1 means no paginantion, return all results
        """
        if object_id:
            object_id = object_id.strip()
            logging.debug('Object ID provided, getting %s', object_id)

            url = 'restapi/%s/%s/%s' % (object_type, method, object_id)
            res = self.__get(url)
            if res:
                return res['results']
            else:
                return None
        elif query:
            if page != -1:
                logging.debug('Fetching %s page of %s for query %s' % (page, object_type, query))
                url = 'search/?db_name=%s&page=%d&%s' % (object_type, page, query)
                res = self.__get(url)
                if res:
                    return res["results"]
                else:
                    return []
            else:
                logging.debug('No page provided, will use pagination to build the response list')
                res_page = [{}]
                res = []
                page = 0
                while len(res_page) != 0:
                    res_page = self.get(object_type=object_type, query=query, method=method, page=page)
                    res += res_page
                    logging.debug('Found %s %s in page %s. Total results: %s', len(res_page), object_type, page, len(res))
                    page += 1

                return res
        else:
            logging.error('No object ID or query provided')
            return None

    def update(self, object_type, object_data):
        """
        Update data in McM
        object_type - [chained_campaigns, chained_requests, campaigns, requests, flows, etc.]
        object_data - new JSON of an object to be updated
        """
        return self.put(object_type, object_data, method='update')

    def put(self, object_type, object_data, method='save'):
        """
        Put data into McM
        object_type - [chained_campaigns, chained_requests, campaigns, requests, flows, etc.]
        object_data - new JSON of an object to be updated
        method - action to be performed, default is 'save'
        """
        url = 'restapi/%s/%s' % (object_type, method)
        res = self.__put(url, object_data)
        return res

    def approve(self, object_type, object_id, level=None):
        if level is None:
            url = 'restapi/%s/approve/%s' % (object_type, object_id)
        else:
            url = 'restapi/%s/approve/%s/%d' % (object_type, object_id, level)

        return self.__get(url)

    def clone_request(self, object_data):
        return self.put('requests', object_data, method='clone')

    def get_range_of_requests(self, query):
        res = self.__put('restapi/requests/listwithfile', data={'contents': query})
        if res:
            return res["results"]
        else:
            return None

    def delete(self, object_type, object_id):
        url = 'restapi/%s/delete/%s' % (object_type, object_id)
        self.__delete(url)

    def forceflow(self, prepid):
        """
        Forceflow a chained request with given prepid
        """
        res = self.__get('restapi/chained_requests/flow/%s/force' % (prepid))
        if res:
            return res["results"]
        else:
            return None
