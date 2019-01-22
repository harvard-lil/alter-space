<template>
  <div>
    <input type="range"
           min="0"
           max="100"
           v-model.lazy.number="volume"/>
  </div>
</template>

<script>
  import EventBus from '../event-bus'

  export default {
    name: "sound-slider",
    components: {},
    methods: {
    },
    watch: {
      volume() {
        console.log("getting value", this.volume);
        EventBus.$emit('update-volume', this.volume);
      }


    },
    data() {
      return {
        audio: undefined,
        volume: 100
      }
    }
  }
</script>

<style scoped>{{}}

</style>