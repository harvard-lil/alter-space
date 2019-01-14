<template>
  <div class="row">
    <div class="col-6">
      <h4>Lights</h4>
      <Lights></Lights>
    </div>
    <div class="col-6">
      <h4>Sounds</h4>
      <Sounds></Sounds>
    </div>
  </div>

</template>

<script>
  import Lights from './Lights'
  import Sounds from './Sounds'

  export default {
    name: "Library",
    components: {Lights, Sounds}
  }
</script>

<style scoped>

</style>