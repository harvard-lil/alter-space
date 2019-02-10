<template>

  <input type="range"
         class="bright-range"
         min="0"
         max="100"
         value="100"
         autocomplete="off"
         v-model.lazy.number="bright"/>
</template>

<script>
  import axios from 'axios'
  import EventBus from '../event-bus';
  const dimUrl = process.env.VUE_APP_BACKEND_URL + "lights" + "/dim"
  export default {
    name: "brightness-slider",
    data() {
      return {
        bright: 100
      }
    },
    watch: {
      bright() {
        let bodyFormData = new FormData();
        bodyFormData.set('id', this.$parent.light);
        bodyFormData.set('bright', this.bright);
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

  }
</script>
