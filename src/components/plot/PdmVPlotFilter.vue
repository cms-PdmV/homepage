<template>
  <div>
    <v-expansion-panels>
      <v-expansion-panel>
        <v-expansion-panel-header>Priority Block Filter</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-checkbox
            class="checkboxmargin"
            v-for="block in dataFilters.blocks"
            v-model="block.selected"
            :key="block.name"
            :label="block.displayName"
          ></v-checkbox>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel>
        <v-expansion-panel-header>Campaign Filter</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-checkbox
            class="checkboxmargin"
            v-for="campaign in dataFilters.campaigns"
            v-model="campaign.selected"
            :key="campaign.name"
            :label="campaign.name"
          ></v-checkbox>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel>
        <v-expansion-panel-header>PWG Filter</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-checkbox
            class="checkboxmargin"
            v-for="pwg in dataFilters.pwgs"
            v-model="pwg.selected"
            :key="pwg.name"
            :label="pwg.name"
          ></v-checkbox>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel>
        <v-expansion-panel-header>Plot Mode</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-radio-group v-model="plotMode">
            <v-radio :key="'change'" :label="'Newly produced'" :value="'change'"></v-radio>
            <v-radio :key="'cumulative'" :label="'Cumulative'" :value="'cumulative'"></v-radio>
          </v-radio-group>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel>
        <v-expansion-panel-header>Plot Scale</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-radio-group v-model="plotScale">
            <v-radio :key="'linear'" :label="'Linear'" :value="'linear'"></v-radio>
            <v-radio :key="'log'" :label="'Logarithmic'" :value="'log'"></v-radio>
          </v-radio-group>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel>
        <v-expansion-panel-header>Bubble Legend</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-radio-group v-model="bubbleLegend">
            <v-radio :key="'off'" :label="'Hidden'" :value="'off'"></v-radio>
            <v-radio :key="'on'" :label="'Visible'" :value="'on'"></v-radio>
          </v-radio-group>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>

import Vue from 'vue'

export default {
  name: 'PdmVPlotFilter',
  data () {
    return {
      dataFilters: {
        blocks: [],
        campaigns: [],
        pwgs: [],
      },
      plotMode: 'change',
      plotScale: 'linear',
      bubbleLegend: 'off'
    }
  },
  created () {

  },
  props: {
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
    this.eventBus.$on('campaignClick', function (campaign) {
      var onlyCurrentSelected = component.dataFilters.campaigns.reduce(function(res, c) {return res && ((c.name === campaign.name) == (c.selected))}, true)
      component.dataFilters.campaigns.map(function(c) {c.selected = (c.name === campaign.name) || onlyCurrentSelected})
    })
  },
  watch: {
    fetchedData () {
      this.prepareFilters()
    },
    dataFilters: {
      handler: function (newVal, oldVal) {
        let enabledBlocks = Object.keys(newVal.blocks).reduce(function(map, key) {
          if (newVal.blocks[key].selected) {
            map.push(newVal.blocks[key].name)
          }
          return map
        }, [])
        let enabledCampaigns = Object.keys(newVal.campaigns).reduce(function(map, key) {
          if (newVal.campaigns[key].selected) {
            map.push(newVal.campaigns[key].name)
          }
          return map
        }, [])
        let enabledPwgs = Object.keys(newVal.pwgs).reduce(function(map, key) {
          if (newVal.pwgs[key].selected) {
            map.push(newVal.pwgs[key].name)
          }
          return map
        }, [])

        this.eventBus.$emit('filterChange', {'campaigns': enabledCampaigns,
                                             'blocks': enabledBlocks,
                                             'pwgs': enabledPwgs})
      },
      deep: true
    },
    plotMode () {
      this.eventBus.$emit('plotModeChange', this.plotMode)
    },
    plotScale () {
      this.eventBus.$emit('plotScaleChange', this.plotScale)
    },
    bubbleLegend () {
      this.eventBus.$emit('bubbleLegendChange', this.bubbleLegend)
    },
  },
  methods: {
    prepareFilters() {
      let newFilters = {}
      newFilters.blocks = []
      newFilters.campaigns = []
      newFilters.pwgs = []
      if (this.fetchedData) {
        for (let campaignName in this.fetchedData.data) {
          newFilters.campaigns.push({'name': campaignName, 'selected': true});
        }
        let availableBlocks = [{'name': 'block1', 'displayName': 'Block 1 (110k)', 'selected': true},
                               {'name': 'block2', 'displayName': 'Block 2 (90k)','selected': true},
                               {'name': 'block3', 'displayName': 'Block 3 (85k)','selected': true},
                               {'name': 'block4', 'displayName': 'Block 4 (80k)','selected': true},
                               {'name': 'block5', 'displayName': 'Block 5 (70k)','selected': true},
                               {'name': 'block6', 'displayName': 'Block 6 (63k)','selected': true},];
        for (let availableBlock of availableBlocks) {
          if (this.fetchedData.blocks.includes(availableBlock.name)) {
            newFilters.blocks.push(availableBlock);
          }
        }
        for (let pwg of this.fetchedData.pwgs) {
          newFilters.pwgs.push({'name': pwg, 'selected': true});
        }
      }
      this.dataFilters = newFilters;
    },
  }
}

</script>

<style>

</style>
