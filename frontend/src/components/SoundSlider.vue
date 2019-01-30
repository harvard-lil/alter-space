<template>

  <div class="col-12">
    <button @click="toggleMute()"
            class="btn-volume"
            :class="{muted: mute}">
    </button>

    <input type="range"
           class="volume-range"
           min="0"
           max="100"
           value="100"
           autocomplete="off"
           v-model.lazy.number="volume"/>
  </div>

</template>

<script>
  import EventBus from '../event-bus'

  export default {
    name: "sound-slider",
    components: {},
    methods: {
      toggleMute() {
        this.mute = !this.mute;
        EventBus.$emit('mute-volume', this.mute);
      }
    },
    watch: {
      volume() {
        EventBus.$emit('update-volume', this.volume);
      }
    },
    data() {
      return {
        audio: undefined,
        volume: 100,
        mute: false
      }
    }
  }
</script>
