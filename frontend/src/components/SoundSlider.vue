<template>

  <div class="row">
    <div class="col-2">
      <button @click="toggleMute()"
              class="btn-volume"
              :class="{muted: mute}">
      </button>
      <label>{{ mute }}</label>
    </div>
    <div class="col-10">
      <input type="range"
             class="volume-range"
             min="0"
             max="100"
             value="100"
             autocomplete="off"
             v-model.lazy.number="volume"/>
      <label class="volume-label">
        Volume
      </label>

    </div>

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
<style scoped>
  input[type="range"] {
    margin-left: -30px;
  }
</style>
