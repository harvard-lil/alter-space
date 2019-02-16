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
    props: ["disable"],
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
        bodyFormData.set('id', this.$parent.light);
        bodyFormData.set('bright', this.bright.toString());
        EventBus.$emit('update-brightness', this.bright);
        axios({
          method: "post",
          url: dimUrl,
          data: bodyFormData,
        }).then(function (results) {
          console.log(results)
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
