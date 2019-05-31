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
        fetch(dimUrl, {
          method: "POST",
          body: bodyFormData,
        }).then((res) => {
          if (!res.ok) {
            throw res;
          }
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
