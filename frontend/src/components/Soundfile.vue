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
        previousVolume: 10,
        selectedSound: false,
        soundPresets: this.$parent.soundPresets,
      }
    },
    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      this.selectedSound = this.soundPresets.indexOf(this.audio) > -1;


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
      this.initializePresetSound();
    },
    methods: {
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
          console.log("getting toggle button of already selected sound", this.audio)
          this.selectedSound = !this.selectedSound;
          this.removeSound();
        } else {
          // send an event out to other sounds so that
          // they may add themselves into the currently playing arena
          // EventBus.$emit("add-new-sound", this.audio);
          this.addSound();
        }
      },
      initializePresetSound() {
        // Plays sound if it's in the presets
        if (this.soundPresets.indexOf(this.audio) > -1) {
          console.log("playing sound", this.audio)
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

