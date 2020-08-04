<template>
  <v-app>
    <v-app-bar app style="background-color: #fff">
      <v-toolbar-title class="headline">
        <span>PdmV</span>
        <span class="font-weight-light">Homepage</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        text
        href="https://cms-pdmv.cern.ch/mcm"
        target="_blank"
        class="d-none d-md-flex"
      >
        <span class="mr-2">McM</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn
        text
        href="https://cms-pdmv.cern.ch/pmp"
        target="_blank"
        class="d-none d-md-flex"
      >
        <span class="mr-2">pMp</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn
        text
        href="https://hypernews.cern.ch/HyperNews/CMS/get/prep-ops.html"
        target="_blank"
        class="d-none d-md-flex"
      >
        <span class="mr-2">HyperNews</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn
        text
        href="https://cms-pdmv.cern.ch/valdb"
        target="_blank"
        class="d-none d-md-flex"
      >
        <span class="mr-2">ValDB</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn
        text
        href="https://cms-pdmv.cern.ch/relmon"
        target="_blank"
        class="d-none d-md-flex"
      >
        <span class="mr-2">RelMon</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <MainComponent/>
    </v-main>
  </v-app>
</template>

<script>
import MainComponent from './components/MainComponent';

export default {
  name: 'App',
  components: {
    MainComponent,
  },
  data: () => ({
    //
  }),
};
</script>
