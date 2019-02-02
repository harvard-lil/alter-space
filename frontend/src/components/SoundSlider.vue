<template>

  <div class="row">
    <div class="col-2">
      <svgicon :icon="icon"
               width="60"
               height="60"
               :original="true"
               class="btn-round"
               @click="toggleMute()"
               stroke="0"></svgicon>
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
  import EventBus from '../event-bus';
  import './icons/volume';
  import './icons/mute';

  export default {
    name: "sound-slider",
    componensts: {},
    methods: {
      toggleMute() {
        this.mute = !this.mute;
        EventBus.$emit('mute-volume', this.mute);
        this.icon = this.mute ? "mute" : "volume"
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
        mute: false,
        icon: "volume"
      }
    }
  }
</script>
<style scoped>
  input[type="range"] {
    margin-left: -30px;
  }
</style>
