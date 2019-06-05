<template>
  <div class="td col-2">
    <svgicon :icon="playLabel"
             width="60"
             height="60"
             :original="true"
             class="btn-round"
             @click="playMusic()"
             stroke="0"></svgicon>

    <label @click="playMusic">{{playLabel}}</label>
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
        play: false,
        playLabel: "play",
      }
    },
    mounted() {
      let self = this;
      this.$on('play-music',(toPlay) => {
        self.play = toPlay;
        self.playLabel = self.play ? "play" : "pause";
      })
    },
    methods: {
      playMusic() {
        this.play = !this.play;
        EventBus.$emit("play-music", this.play);
        this.playLabel = this.play ? "play" : "pause";
      }
    }
  }
</script>
