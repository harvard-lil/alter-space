<template>
  <div :selectedSound="selectedSound"
       :audio="audio">
    <button @click="toggleButton"
            class="toggle"
            v-bind:class="{ on: toggle }">
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
    props: ['audio', 'soundType'],
    name: "soundfile",
    data() {
      return {
        audioBaseUrl: audioBaseUrl,
        toggle: false,
        audioName: this.$parent.$parent.getAudioName(this.audio),
        audioPath: audioBaseUrl + this.soundType + "/" + this.audio,
        play: false,
        previousVolume: 10,
        selectedSound: false
      }
    },
    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      this.selectedSound = this.$parent.allSoundsOfType.indexOf(this.audio) > -1;


      // catch global event, check if this is the sound we're trying to add
      EventBus.$on('add-new-sound', (sound_name) => {
        if (this.audio === sound_name && this.selectedSound) {
          this.play = true;
          this.selectedSound = true;
          this.$parent.allSoundsOfType[this.soundType].push(this.audio);
        }
      });

      EventBus.$on('pause-music', () => {
        if (this.selectedSound) {
          this.toggleButton()
        }
      });

      EventBus.$on('update-volume', (volume) => {
        if (this.selectedSound) {
          this.audioFile.volume = volume / 100;
          this.previousVolume = volume;
        }
      });

      EventBus.$on('mute-volume', (mute) => {
        if (this.selectedSound) {
          this.audioFile.volume = mute ? 0 : this.previousVolume / 100
        }
      });
      this.initializePresetSound()
    },
    methods: {
      toggleButton() {
        if (this.selectedSound) {
          this.toggle = !this.toggle;
          this.toggle ? this.audioFile.play() : this.audioFile.pause();
        } else {
          // send an event out to other sounds so that
          // they may add themselves into the currently playing arena
          EventBus.$emit("add-new-sound", this.audio);
        }
      },
      showChosenSound() {

        this.toggleButton();
      },
      initializePresetSound() {
        // Plays sound if it's in the presets
        if (this.selectedSound) this.showChosenSound();
      }
    },
    beforeDestroy() {
      this.selectedSound = false;
    }
  }
</script>

