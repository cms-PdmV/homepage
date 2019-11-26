<template>
  <table style="width:100%" class="elevation-2">
    <tr>
      <th>Campaign</th><th>Events</th><th>pMp Links</th><th>McM Links</th>
    </tr>
    <tr v-for="campaignData in rows"
        :key="campaignData.name"
        :class="[((hoverCampaignClass !== undefined) && (hoverCampaignClass == campaignData.data.class)) ? 'hovering' : '', campaignData.data.class, 'campaign-row']"
        @mouseover="handleHoverOver(campaignData.data)"
        @mouseleave="handleHoverOver(undefined)"
        v-bind:style="getRowStyle(campaignData)">
      <td style="text-align: left; word-break: break-all;" @mousedown="handleRowClick(campaignData)">{{campaignData.name}}</td>
      <td style="text-align: right;" @mousedown="handleRowClick(campaignData)" :title="campaignData.data.sum"><b>{{campaignData.data.niceSum}}</b></td>
      <td><a target="_blank" :href="'https://cms-pdmv.cern.ch/pmp/present?r=' + campaignData.name + '&growingMode=true&mode=events&groupBy='">Present</a>&nbsp;
          <a target="_blank" :href="'https://cms-pdmv.cern.ch/pmp/historical?r=' + campaignData.name">Historical</a>
      </td>
      <td>
        <span v-if="campaignData.data.type !== 'rereco'" v-for="pwgName in campaignData.data.pwgs">
          <a target="_blank" :href="'https://cms-pdmv.cern.ch/mcm/requests?member_of_campaign=' + campaignData.name + '&pwg=' + pwgName">{{pwgName}}</a>&nbsp;
        </span>
      </td>
    </tr>
    <tr style="opacity: 0.6" v-if="rows.length > 1 && plotData.summary.monteCarloSum > 0 && plotData.summary.rerecoSum > 0">
      <td style="text-align: left; word-break: break-all;"><i>Total Monte Carlo</i></td>
      <td style="text-align: right;"><b>{{plotData.summary.monteCarloNiceSum}}</b></td>
    </tr>
    <tr style="opacity: 0.6" v-if="rows.length > 1 && plotData.summary.monteCarloSum > 0 && plotData.summary.rerecoSum > 0">
      <td style="text-align: left; word-break: break-all;"><i>Total Data ReReco</i></td>
      <td style="text-align: right;"><b>{{plotData.summary.rerecoNiceSum}}</b></td>
    </tr>
    <tr style="opacity: 0.6" v-if="rows.length > 1 && (plotData.summary.monteCarloSum > 0 || plotData.summary.rerecoSum > 0)">
      <td style="text-align: left; word-break: break-all;"><i>Total</i></td>
      <td style="text-align: right;"><b>{{plotData.summary.totalNiceSum}}</b></td>
    </tr>
  </table>
</template>

<script type="text/javascript">
  import Vue from 'vue'
  import * as d3 from 'd3'
  import md5 from 'js-md5'
  import dateFormat from 'dateformat'

  export default {
    name: 'PdmVTable',
    // svg cannot be property by itself, changes object type during assignment, within ddd object is fine
    data () {
      return {
        rows: [],
        hoverCampaignClass: undefined,
        filterPwgs: [],
      }
    },
    props: {
      plotData: {
        type: Object,
        default: () => {}
      },
      eventBus: {
        type: Object,
        default: () => undefined
      }
    },
    mounted () {
      let component = this
      this.eventBus.$on('campaignHover', function(campaign) {
        if (campaign !== undefined && campaign.class) {
          component.hoverCampaignClass = campaign.class;
        } else {
          component.hoverCampaignClass = undefined;
        }
      })
      this.eventBus.$on('filterChange', function(filters) {
        component.filterPwgs = filters.pwgs.filter(el => el.toLowerCase() !== 'rereco');
      })
    },
    watch: {
      plotData () {
        this.timestamps = this.plotData.timestamps;
        this.rows = [];
        for (let campaignName in this.plotData.data) {
          this.rows.push({'name': campaignName, 'data': this.plotData.data[campaignName]})
        }
        this.rows = this.rows.sort(function(a, b) { return a.data.sum > b.data.sum ? -1 : 1})
      }
    },
    methods: {
      handleHoverOver(campaignData) {
        this.eventBus.$emit('campaignHover', campaignData)
      },
      handleRowClick(campaignData) {
        this.eventBus.$emit('campaignClick', campaignData)
      },
      getRowStyle(campaignData) {
        if (this.hoverCampaignClass === campaignData.data.class) {
          return {background: campaignData.data.color,
                  color: '#fff'}
        }
      }
    }
  };

</script>

<style scoped>
  table {
    border-collapse: collapse;
    margin: auto;
  }

  table, th, td {
    border: 1px solid rgba(0, 0, 0, 0.12);;
    padding: 4px;
    text-align: center;
  }

  .campaign-row {
    cursor: pointer;
  }

  .hovering a {
    color: white;
  }
</style>