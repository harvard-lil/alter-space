<template>

  <input type="range"
         class="bright-range"
         min="0"
         max="100"
         value="100"
         autocomplete="off"
         :disabled="disable"
         v-model.lazy.number="bright"/>
</template>

<script>
  import axios from 'axios'
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

        let bodyFormData = new FormData();
        if (this.light) {
          bodyFormData.set('label', this.light);
        }
        bodyFormData.set('bright', this.bright.toString());
        EventBus.$emit('update-brightness', this.bright);
        this.$parent.disableColors = true;
        this.$parent.disableEffect = true;
        let self = this;
        axios({
          method: "post",
          url: dimUrl,
          data: bodyFormData,
        }).then(()=>{
          self.$parent.disableColors = false;
          self.$parent.disableEffect = false;
        })

      }
    },
    mounted() {
      let self = this;
      EventBus.$on('reset-brightness', function() {
        self.updateBrightness();
      })
    }

  }
</script>
