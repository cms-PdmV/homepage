<template>
  <v-app>
    <v-container>
      <v-row>
        <v-col cols="12">
          <PdmVPlot :fetchedData="fetchedData"></PdmVPlot>
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
  </v-app>
</template>

<script>

import PdmVPlot from './plot/PdmVPlot.vue'
import PdmVHierarchy from './hierarchy/PdmVHierarchy.vue'
import PdmVTerms from './terms/PdmVTerms.vue'
import axios from 'axios'

export default {
  name: 'MainComponent',
  data () {
    return {
      fetchedData: {}
    }
  },
  created () {
    axios.get('file.json').then(response => {
      this.fetchedData = response.data;
    });
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

<style scoped>

</style>
