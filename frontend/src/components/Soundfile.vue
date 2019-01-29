<template>
  <div :currentlyPlaying="currentlyPlaying"
       :audio="audio">
    <button @click="toggleButton" class="toggle" v-bind:class="{ on: toggle }">
      {{ audioName }}
    </button>
    <!-- audio files are hidden from DOM / view -->
    <audio loop controls>
      <source :id="audio" :src="`${audioPath}`" type="audio/mpeg">
    </audio>
  </div>
</template>

<script>
  import EventBus from '../event-bus';

  const audioBaseUrl = process.env.VUE_APP_SOUND_URL;

  export default {
    props: ['audio', 'showToggles', 'soundType'],
    name: "soundfile",
    data() {
      return {
        audioBaseUrl: audioBaseUrl,
        toggle: false,
        audioName: this.$parent.$parent.getAudioName(this.audio),
        audioPath: audioBaseUrl + this.soundType + "/" + this.audio,
        play: false,
        currentlyPlaying: false,
        previousVolume: 10
      }
    },
    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      // catch global event, check if this is the sound we're trying to add
      EventBus.$on('add-new-sound', (sound_name) => {
        if (this.audio === sound_name && this.showToggles) {
          this.play = true;
          this.$parent.$parent.soundPresets[this.soundType].push(this.audio);
        }
      });

      EventBus.$on('pause-music', () => {
        if (this.showToggles && this.currentlyPlaying) {
          this.toggleButton()
        }
      });

      EventBus.$on('update-volume', (volume) => {
        if (this.showToggles && this.currentlyPlaying) {
          this.audioFile.volume = volume / 100;
          this.previousVolume = volume;
        }
      });

      EventBus.$on('mute-volume', (mute) => {
        if (this.showToggles && this.currentlyPlaying) {
          this.audioFile.volume = mute ? 0 : this.previousVolume / 100
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
          EventBus.$emit("add-new-sound", this.audio);
        }
      },
      showChosenSound() {
        if (this.$parent.$parent.soundPresets[this.soundType].indexOf(this.audio) > -1) {
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

