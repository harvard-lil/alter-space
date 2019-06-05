<template>
  <div class="td col-2">
    <svgicon :icon="playLabel"
             width="60"
             height="60"
             :original="true"
             :class="playLabel"
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

    beforeMount() {
      EventBus.$on("play-music", (toPlay) => {
        this.play = toPlay;
        this.setPlayLabel();
      })
    },
    methods: {
      setPlayLabel() {
        this.playLabel = this.play ? "pause" : "play";
      },
      playMusic() {
        this.play = !this.play;
        EventBus.$emit("play-music", this.play);
        this.setPlayLabel();
      }
    }
  }
</script>
