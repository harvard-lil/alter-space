<template>
  <button class="btn-default btn-music"
          v-bind:class="{ pause: pause}"
          @click="pauseMusic">
  </button>

</template>

<script>
  import EventBus from '../event-bus'

  export default {
    name: "play-button",
    data() {
      return {
        pause: false,
      }
    },
    methods: {
      pauseMusic() {
        this.pause = !this.pause;
        EventBus.$emit("pause-music", this.pause);
      }
    }
  }
</script>
