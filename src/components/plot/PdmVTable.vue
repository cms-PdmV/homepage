<template>
  <table style="width:100%" class="elevation-2">
    <tr>
      <td>Campaign</td><td>Events</td><td>Campaign Links</td><td>McM Links</td>
    </tr>
    <tr v-for="campaignData in rows"
        :key="campaignData.name"
        :class="[((hoverCampaignClass !== undefined) && (hoverCampaignClass == campaignData.data.class)) ? 'hovering' : '', campaignData.data.class, 'campaign-row']"
        @mouseover="handleHoverOver(campaignData.data)"
        @mouseleave="handleHoverOver(undefined)"
        v-bind:style="getRowStyle(campaignData)">
      <td style="text-align: left; word-break: break-all;" @mousedown="handleRowClick(campaignData)">{{campaignData.name}}</td>
      <td style="text-align: right;" @mousedown="handleRowClick(campaignData)" :title="campaignData.data.sum"><b>{{campaignData.data.niceSum}}</b></td>
      <td><a target="_blank" :href="'https://cms-pdmv.cern.ch/pmp/historical?r=' + campaignData.name">pMp</a>&nbsp;
          <a target="_blank" :href="'https://twiki.cern.ch/twiki/bin/view/CMS/' + campaignData.name">TWiki</a></td>
      <td>
        <span v-for="pwgName in campaignPwgs[campaignData.name]">
          <a target="_blank" :href="'https://cms-pdmv.cern.ch/mcm/requests?member_of_campaign=' + campaignData.name + '&pwg=' + pwgName">{{pwgName}}</a>&nbsp;
        </span>
      </td>
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
        campaignPwgs: {},
        hoverCampaignClass: undefined,
        filterPwgs: [],
      }
    },
    props: {
      plotData: {
        type: Object,
        default: () => {}
      },
      fetchedData: {
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
        for (let campaignName in this.fetchedData.data) {
          this.campaignPwgs[campaignName] = Object.keys(this.fetchedData.data[campaignName]).filter(el => this.filterPwgs.includes(el))
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