<template>

  <input type="range"
         class="bright-range"
         min="50"
         max="100"
         value="100"
         autocomplete="off"
         :disabled="disable"
         v-model.lazy.number="bright"/>
</template>

<script>
  import axios from 'axios';


  import EventBus from '../event-bus';

  const dimUrl = process.env.VUE_APP_BACKEND_URL + "lights" + "/dim"
  export default {
    name: "brightness-slider",
    props: ["disable", "light"],
    data() {
      return {
        bright: 100
      }
    },
    watch: {
      bright() {
        this.updateBrightness();
      }
    },
    methods: {
      updateBrightness() {
        let data = {
          bright: this.bright.toString()
        };
        // if it's universal brightness, no light is set
        if (this.light)
          data.label = this.light;
        EventBus.$emit('update-brightness', this.bright);
        this.$parent.disableColors = true;
        this.$parent.disableEffect = true;
        let self = this;
        axios({
          method: "post",
          url: dimUrl,
          data: data,
        }).then(() => {
          self.$parent.disableColors = false;
          self.$parent.disableEffect = false;
        })

      }
    },
    mounted() {
      let self = this;
      EventBus.$on('reset-brightness', function () {
        self.updateBrightness();
      })
    },

  }
</script>
