<template>
  <div class="sound-container"
       :showToggles="showToggles"
       :currentlyPlaying="currentlyPlaying"
       :index="index">
    <button @click="toggleButton" class="toggle" v-bind:class="{ on: toggle }">
      {{ audioName }}
    </button>
    <!-- audio files are hidden from DOM / view -->
    <audio loop controls>
      <source :id="audio" :src="`${audio}`" type="audio/mpeg">
    </audio>
  </div>
</template>

<script>
  import EventBus from '../event-bus';

  const audioBaseUrl = process.env.VUE_APP_BACKEND_URL + "sounds";

  function getAudioName(audioPath) {
    let parts = audioPath.split('/');
    return parts[parts.length - 1]
  }

  export default {
    props: ['audio', 'showToggles', 'index'],
    name: "soundfile",
    data() {
      return {
        audioBaseUrl: audioBaseUrl,
        toggle: false,
        audioName: getAudioName(this.audio),
        play: false,
        currentlyPlaying: false,
      }
    },
    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      // catch global event, check if this is the sound we're trying to add
      EventBus.$on('add-new-sound', (sound_index) => {
        if (this.index === sound_index && this.showToggles) {

          this.play = true;
          this.toggleButton()
        }
      });

      EventBus.$on('pause-music', (pause) => {
        if (this.showToggles && this.currentlyPlaying) {
          this.toggleButton()
        }
      });

      this.initializePresetSound()
    },
    methods: {
      toggleButton() {
        if (this.showToggles) {
          this.toggle = !this.toggle;
          this.toggle ? this.audioFile.play() : this.audioFile.pause();
        } else {
          // send an event out to other sounds so that
          // they may add themselves into the currently playing arena
          EventBus.$emit("add-new-sound", this.index);
        }
      },
      showChosenSound() {
        if (this.$parent.$parent.soundPresets.indexOf(this.index) > -1) {
          this.toggleButton();
          this.currentlyPlaying = true;
        }
      },
      initializePresetSound() {
        // Plays sound if it's in the presets
        if (this.showToggles) this.showChosenSound();

      }
    },
    beforeDestroy() {
      this.currentlyPlaying = false;
    }
  }
</script>

