<template>
  <div style="background: white;" class="pa-2 elevation-3">
    <h1 class="ml-2">PdmV Organigram</h1>
    <div style="text-align: center;">
      <a href="hierarchy.png">
        <img :src="'hierarchy.png'">
      </a>
    </div>
  </div>
</template>

<script type="text/javascript">

  export default {
    name: 'PdmVHierarchy',
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

img {
  max-width: 80%;
  margin: auto;
  max-height: 500px;
}

</style>