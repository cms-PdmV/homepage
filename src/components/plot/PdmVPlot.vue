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
            :fetchedData="fetchedData"
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
  </div>
</template>

<script>

import * as d3 from 'd3'
import PdmVBarChart from './PdmVBarChart.vue'
import PdmVTable from './PdmVTable.vue'
import PdmVPlotFilter from './PdmVPlotFilter.vue'
import md5 from 'js-md5'
import Vue from 'vue'


export default {
  name: 'MainComponent',
  data () {
    return {
      bus: new Vue(),
      plotData: {},
    }
  },
  created () {
  },
  mounted () {
    let component = this
    this.bus.$on('filterChange', function (filters) {
      component.prepareData(filters)
    })
  },
  props: {
    fetchedData: {
      type: Object,
      default: () => {}
    }
  },
  watch: {

  },
  components: {
    PdmVBarChart,
    PdmVTable,
    PdmVPlotFilter
  },
  methods: {
    prepareData(filters) {
      var newData = {}      
      for (let campaignName of filters.campaigns) {
        let campaignData = this.fetchedData.data[campaignName];
        let md5CampaignName = md5(campaignName);
        let campaignClass = 'campaign-' + md5CampaignName;
        let campaignColor = this.stringToColor(md5CampaignName);
        var campaign = {'name': campaignName,
                        'class': campaignClass,
                        'color': campaignColor,
                        'values': new Array(this.fetchedData.timestamps.length - 1).fill(0)}
        for (let pwg of filters.pwgs) {
          if (!(pwg in campaignData)) {
            continue
          }
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
          campaign['niceSum'] = this.formatBigNumber(campaign['sum'])
          newData[campaignName] = campaign;
        }
      }
      this.plotData = {'data': newData, 'timestamps': this.fetchedData.timestamps}
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
