<template>
  <div class="btn-group btn-group-color"
       role="group"
       aria-label="color button group">

    <button type="button"
            class="btn-round btn-color"
            :style="{'backgroundColor': color1}">
    </button>
    <button type="button"
            class="btn-round btn-color"
            :style="{'backgroundColor': color2}">
    </button>
    <button type="button"
            class="btn-round btn-color"
            :style="{'backgroundColor': color3}">
    </button>
  </div>

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