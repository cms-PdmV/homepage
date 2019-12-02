<template>
  <div class="elevation-3 pa-2" style="background: white">
    <h1 class="ml-2">Event Production</h1>
    <v-row>
      <v-col xs="12" sm="12" md="12" lg="12" cols="12">
        <div class="pa-2">
          <PdmVBarChart
            style="margin: auto;"
            :plotData="plotData"
            :eventBus="bus">
          </PdmVBarChart>
        </div>
      </v-col>
      <v-col xs="12" sm="12" md="12" lg="8" cols="12">
        <div class="pa-2">
          <PdmVTable
            :plotData="plotData"
            :eventBus="bus">
          </PdmVTable>
        </div>
      </v-col>
      <v-col xs="12" sm="12" md="12" lg="4" cols="12">
        <div class="pa-2">
          <PdmVPlotFilter
            :fetchedData="fetchedData"
            :eventBus="bus">
          </PdmVPlotFilter>
        </div>
      </v-col>
    </v-row>
    <small style="opacity: 0.4">For Monte Carlo production, only MiniAOD and NanoAOD campaigns are shown</small>
  </div>
</template>

<script>

import * as d3 from 'd3'
import PdmVBarChart from './PdmVBarChart.vue'
import PdmVTable from './PdmVTable.vue'
import PdmVPlotFilter from './PdmVPlotFilter.vue'
import md5 from 'js-md5'
import Vue from 'vue'
import axios from 'axios'


export default {
  name: 'MainComponent',
  data () {
    return {
      bus: new Vue(),
      fetchedData: {},
      plotData: {'summary': {}},
    }
  },
  created () {
    this.fetchData();
  },
  mounted () {
    let component = this
    this.bus.$on('filterChange', function (filters) {
      component.prepareData(filters)
    })
    this.bus.$on('timeRangeChange', function (timeRange) {
      component.fetchData(timeRange);
    })
  },
  props: {
  },
  watch: {

  },
  components: {
    PdmVBarChart,
    PdmVTable,
    PdmVPlotFilter
  },
  methods: {
    fetchData(timeRange) {
      let component = this;
      if (timeRange === undefined) {
        timeRange = 'week';
      }
      axios.get(timeRange + '.json').then(response => {
        component.fetchedData = response.data;
      });
    },
    prepareData(filters) {
      var newData = {}
      var monteCarloSum = 0;
      var rerecoSum = 0;
      for (let campaignName of filters.campaigns) {
        let campaignData = this.fetchedData.data[campaignName];
        let md5CampaignName = md5(campaignName);
        let campaignClass = 'campaign-' + md5CampaignName;
        let campaignColor = this.stringToColor(md5CampaignName);
        var campaign = {'name': campaignName,
                        'class': campaignClass,
                        'color': campaignColor,
                        'values': new Array(this.fetchedData.timestamps.length - 1).fill(0),
                        'pwgs': []}
        for (let pwg of filters.pwgs) {
          if (!(pwg in campaignData)) {
            continue
          }
          campaign['pwgs'].push(pwg);
          for (let blockName of filters.blocks) {
            if (!(blockName in campaignData[pwg])) {
              continue
            }
            for (let i = 0; i < campaignData[pwg][blockName].length; i++) {
              campaign.values[i] += campaignData[pwg][blockName][i];
            }
          }
        }
        campaign['sum'] = d3.sum(campaign.values);
        if (campaign['sum'] > 0) {
          if (campaign['pwgs'].length === 1 && campaign['pwgs'][0].toLowerCase() === 'rereco') {
            campaign['type'] = 'rereco'
            rerecoSum += campaign['sum']
          } else {
            campaign['type'] = 'mc'
            monteCarloSum += campaign['sum']
          }
          campaign['niceSum'] = this.formatBigNumber(campaign['sum'])
          newData[campaignName] = campaign;
        }
      }
      this.plotData = {'data': newData,
                       'timestamps': this.fetchedData.timestamps,
                       'summary': {'monteCarloSum': monteCarloSum,
                                   'monteCarloNiceSum': this.formatBigNumber(monteCarloSum),
                                   'rerecoSum': rerecoSum,
                                   'rerecoNiceSum': this.formatBigNumber(rerecoSum),
                                   'totalSum': monteCarloSum + rerecoSum,
                                   'totalNiceSum': this.formatBigNumber(monteCarloSum + rerecoSum)}}
    },
    stringToColor(str) {
      var hash1 = 0;
      var hash2 = 1;
      for (var i = 0; i < str.length; i++) {
        hash1 += str.charCodeAt(i);
        hash2 = (hash2 * str.charCodeAt(i)) % 11716593810022656 + 1;
      }
      hash1 = hash1 % 300 + 60;
      hash2 = (hash2 % 4) * 8 + 45;
      return 'hsl(' + hash1 + ',' + hash2 + '%,'+ (100 - hash2)+'%)'
    },
    formatBigNumber (number) {
      var result = ''
      if (number >= 1e9) {
          result = (Math.round(number / 10000000.0) / 100.0).toFixed(2) + "G"
      } else if (number >= 1e6) {
          result = (Math.round(number / 10000.0) / 100.0).toFixed(2) + "M"
      } else if (number >= 1e3) {
          result = (Math.round(number / 10.0) / 100.0).toFixed(2) + "k"
      } else {
          result = number.toString()
      }
      return result.replace('.00', '')
                   .replace('.10', '.1')
                   .replace('.20', '.2')
                   .replace('.30', '.3')
                   .replace('.40', '.4')
                   .replace('.50', '.5')
                   .replace('.60', '.6')
                   .replace('.70', '.7')
                   .replace('.80', '.8')
                   .replace('.90', '.9')
    },
    handleFilterChange(filters) {
      this.dataFilters = filters;
      this.prepareData(this.dataFilters)
    }
  }
}

</script>

<style scoped>

</style>
