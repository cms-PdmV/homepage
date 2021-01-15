<template>
  <div style="background-color: #fafafa">
    <v-container>
      <v-row>
        <v-col cols="12">
          <PdmVPlot></PdmVPlot>
        </v-col>
      </v-row>
      <v-row>
        <v-col xs="12" sm="12" md="7" lg="6" cols="12">
          <PdmVHierarchy></PdmVHierarchy>
        </v-col>
        <v-col xs="12" sm="12" md="5" lg="6" cols="12">
          <PdmVTerms></PdmVTerms>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>

import PdmVPlot from './plot/PdmVPlot.vue'
import PdmVHierarchy from './hierarchy/PdmVHierarchy.vue'
import PdmVTerms from './terms/PdmVTerms.vue'

export default {
  name: 'MainComponent',
  data () {
    return {
    }
  },
  created () {

  },
  watch: {

  },
  components: {
    PdmVPlot,
    PdmVHierarchy,
    PdmVTerms
  },
  methods: {

  }
}
</script>

<style>

@media only screen and (max-width: 600px) {
  .row > div {
    padding-left: 0;
    padding-right: 0;
  }

  .container {
    padding: 0;
  }

  .row {
    margin-right: 0;
    margin-left: 0;
  }
}

</style>
