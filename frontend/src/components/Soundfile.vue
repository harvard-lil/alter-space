<template>
  <div :selectedSound="selectedSound"
       :audio="audio">
    <button @click="toggleButton()"
            class="btn-toggle"
            v-bind:class="{ on: selectedSound }">
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
        audioName: this.$parent.$parent.getAudioName(this.audio),
        audioPath: audioBaseUrl + this.soundType + "/" + this.audio,
        play: false,
        previousVolume: 100,
        selectedSound: false,
        soundPresets: this.$parent.soundPresets,
      }
    },
    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      this.selectedSound = this.soundIsInChosenField();


      EventBus.$on('pause-music', (tryingToPause) => {
        if (this.soundIsInChosenField()) {
          tryingToPause ? this.pauseSound() : this.playSound();
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
      this.initializePresetSound();
    },
    methods: {
      soundIsInChosenField() {
        return this.soundPresets.indexOf(this.audio) > -1;
      },
      addSound() {
        this.play = true;
        this.selectedSound = true;
        this.soundPresets.push(this.audio);
        this.playSound()

      },
      removeSound() {
        let index = this.soundPresets.indexOf(this.audio);
        this.soundPresets.splice(index, 1);
        this.pauseSound();
      },
      pauseSound() {
        this.audioFile.pause();
      },
      playSound() {
        this.audioFile.play()
      },

      toggleButton() {
        if (this.selectedSound) {
          this.selectedSound = !this.selectedSound;
          this.removeSound();
        } else {
          this.addSound();
        }
      },
      initializePresetSound() {
        // Plays sound if it's in the presets
        if (this.soundIsInChosenField()) {
          this.selectedSound = true;
          this.play = true;
          this.playSound();
        }

      }
    },
    beforeDestroy() {
      this.selectedSound = false;
      this.pauseSound();
    }
  }
</script>

