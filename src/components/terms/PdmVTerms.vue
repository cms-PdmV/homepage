<template>
  <div style="background: white;" class="pa-2 elevation-3">
    <h1 class="ml-2">Important Links</h1>
    <ul>
      <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/mcm/'">McM</a> - Monte Carlo management website</li>
      <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/pmp/'">pMp</a> - Production monitoring website</li>
      <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/stats/'">Stats</a> - PdmV cache of ReqMgr2 and DBS</li>
      <li><a target="_blank" :href="'https://twiki.cern.ch/twiki/bin/view/CMS/PdmV'">TWiki</a> - PdmV TWiki</li>
      <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/relmon/'">RelMon</a> - RelMon reports</li>
      <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/valdb/'">ValDB</a> - Validation reports</li>
    </ul>
  </div>
</template>

<script type="text/javascript">

  export default {
    name: 'PdmVTerms',
    // svg cannot be property by itself, changes object type during assignment, within ddd object is fine
    data () {
      return {

      }
    },

    props: {

    },

    watch: {

    },
    methods: {

    },
    mounted () {

    }
  };

</script>

<style scoped>

</style>