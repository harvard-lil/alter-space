<template>
  <div class="td col-2">
    <loader :typeOfLoader="'playbutton'"
            v-if="loading && !loadedAudio">
    </loader>
    <svgicon :icon="playLabel"
             v-if="!loading || loadedAudio"
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
  import Loader from "./Loader";

  export default {
    name: "play-button",
    components: {
      Loader
    },
    data() {
      return {
        play: false,
        playLabel: "play",
        loading: false,
        loadedAudio: false,
        loadedOnce: false
      }
    },

    beforeMount() {
      EventBus.$on("play-music", (toPlay) => {
        this.play = toPlay;
        this.setPlayLabel();
      });
      EventBus.$on('sound-loaded', () => {
        this.loading = false;
        this.loadedAudio = true;
        this.playLabel = "pause";
      })

    },
    methods: {
      setPlayLabel() {
        this.playLabel = this.play ? "pause" : "play";
      },
      playMusic() {
        this.play = !this.play;
        if (this.play && !this.loadedOnce) {
          this.loading = true;
          this.loadedAudio = false;
          this.playLabel = "loading...";
        }
        this.loadedOnce = true;
        EventBus.$emit("play-music", this.play);
        this.setPlayLabel();
      }
    }
  }
</script>
