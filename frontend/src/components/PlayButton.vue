<template>
  <div>
    <svgicon :icon="playLabel"
             width="60"
             height="60"
             :original="true"
             class="btn-round"
             @click="pauseMusic()"
             stroke="0"></svgicon>

    <label @click="pauseMusic">{{playLabel}}</label>
  </div>
</template>

<script>
  import EventBus from '../event-bus';
  import "./icons/play";
  import "./icons/pause";

  export default {
    name: "play-button",
    data() {
      return {
        pause: false,
        playLabel: "pause",
      }
    },
    methods: {
      pauseMusic() {
        this.pause = !this.pause;
        EventBus.$emit("pause-music", this.pause);
        this.playLabel = this.pause ? "play" : "pause"
      }
    }
  }
</script>
