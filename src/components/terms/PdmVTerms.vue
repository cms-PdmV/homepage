<template>
  <div style="background: white;" class="pa-2 elevation-3">
    <h1 class="ml-2">Important Links</h1>
    <ul>
      <li>Monte Carlo
        <ul>
          <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/mcm/'">McM</a> - Monte Carlo management website. Main tool for creating, joining and submitting MC requests</li>
          <li><a target="_blank" :href="'https://monte-carlo-production-tools.gitbook.io/project/'">Monte Carlo knowledge base</a> - useful technical information for MC contacts and MC requests managers working in PdmV
            <ul>
              <li><a target="_blank" :href="'https://monte-carlo-production-tools.gitbook.io/project/mccontact'">MC contact's corner</a> - useful information for Monte Carlo contacts about how to act in McM</li>
              <li><a target="_blank" :href="'https://monte-carlo-production-tools.gitbook.io/project/analyzers-corner'">MC analyzer's corner</a> - basic explanation of the glossary, needed for analysers to understand the logic of the central MC production</li>
            </ul>
          </li>
          <li><a target="_blank" :href="'https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMcCampaigns  '">Campaigns TWiki</a> - Monte Carlo campaigns TWiki</li>        
          <li><a target="_blank" :href="'https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable'">Analysis Table</a> - analysis guideline</li>
          <li><a target="_blank" :href="'https://hypernews.cern.ch/HyperNews/CMS/get/prep-ops.html'">MC HyperNews</a> - forum dedicated to the discussion and advertisement of requests managed within the McM</li>
        </ul>
      </li>
      <li>Data ReReco
        <ul>
          <li><a target="_blank" :href="'https://twiki.cern.ch/twiki/bin/view/CMS/PdmVDataReprocessing'">Reprocessing TWiki</a> - information about data reprocessing in PdmV</li>
        </ul>
      </li>
      <li>Release Validation
        <ul>
          <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/relmon/'">RelMon</a> - RelMon reports</li>
          <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/valdb/'">ValDB</a> - Validation reports</li>
        </ul>
      </li>
      <li>Misc
        <ul>
          <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/pmp/'">pMp</a> - Production monitoring website</li>
          <li><a target="_blank" :href="'https://cms-pdmv.cern.ch/stats/'">Stats</a> - PdmV cache of ReqMgr2 and DBS</li>
          <li><a target="_blank" :href="'https://twiki.cern.ch/twiki/bin/view/CMS/PdmV'">TWiki</a> - PdmV TWiki</li>
        </ul>
      </li>
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
