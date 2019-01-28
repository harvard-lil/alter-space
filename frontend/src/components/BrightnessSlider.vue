<template>
  <div class="row">

    <input type="range"
           class="bright-range"
           min="0"
           max="100"
           value="100"
           autocomplete="off"
           v-model.lazy.number="bright"/>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: "BrightnessSlider",
    data() {
      return {
        bright: 50
      }
    },
    watch: {
      bright() {
        // TODO: post to light endpoint
      }
    },

  }
</script>

<style scoped>

</style>