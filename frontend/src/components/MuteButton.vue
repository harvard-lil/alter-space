<template>
    <div class="td col-2">
    <svgicon :icon="icon"
             width="60"
             height="60"
             :original="true"
             class="btn-round"
             @click="toggleMute()"
             stroke="0"></svgicon>

    <label>{{ muteLabel }}</label>
  </div>

</template>

<script>
  import EventBus from '../event-bus';
  import './icons/mute';
  import './icons/volume';


  export default {
    name: "mute-button",
    methods: {
      toggleMute() {
        this.mute = !this.mute;
        this.muteLabel = this.mute ? "unmute" : "mute";
        EventBus.$emit('mute-volume', this.mute);
        this.icon = this.mute ? "mute" : "volume"
      }
    },
    data() {
      return {
        icon: "volume",
        mute: false,
        muteLabel: 'mute'
      }
    }


  }
</script>

<style scoped>

</style>