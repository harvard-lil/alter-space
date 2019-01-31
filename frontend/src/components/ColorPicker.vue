<template>


</template>

<script>
  import axios from 'axios';
  export default {
    name: "ColorPicker",
    data() {
      return {
        hexVal: "#ffffff",
        src: require('../assets/img/colorwheel.jpg'),
        showColorPicker: false,
        color1: "#ff6666",
        color2: "#fbd6e8",
        color3: "#fbb03b",
      }
    },
    methods: {
      getPresetColors() {
        axios.get("")
      }
    },
    mounted: function () {
      this.getPresetColors();
    }
  }
</script>

<style scoped>

</style>