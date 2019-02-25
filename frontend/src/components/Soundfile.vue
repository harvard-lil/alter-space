<template>
  <div :selectedSound="selectedSound"
       :audio="audio">
    <button @click="toggleButton()"
            class="btn-toggle btn-sound-add"
            v-bind:class="{ on: selectedSound }">
      {{ audioName }}
    </button>
    <br/>
    <input type="range"
           class="col-centered slider-small"
           :disabled="selectedSound === false"
           min="1"
           max="100"
           value="50"
           autocomplete="off"
           v-model.lazy.number="volume"/>
    <!-- audio files are hidden from DOM / view -->
    <audio loop controls preload="none">
      <source :id="audio" :src="`${audioPath}`" type="audio/mpeg">
    </audio>
  </div>
</template>

<script>
  import EventBus from '../event-bus';

  const audioBaseUrl = process.env.VUE_APP_SOUND_LOCATION === "LOCAL" ? process.env.VUE_APP_SOUND_LOCAL_URL : process.env.VUE_APP_SOUND_REMOTE_URL;
  // eslint-disable-next-line
  console.log(audioBaseUrl);

  export default {
    props: ['audio', 'soundType'],
    name: "soundfile",
    data() {
      return {
        audioBaseUrl: audioBaseUrl,
        audioName: this.$parent.$parent.getAudioName(this.audio),
        audioPath: audioBaseUrl + this.soundType + "/" + this.audio,
        previousVolume: 100,
        selectedSound: false,
        soundPresets: this.$parent.soundPresets,
        pause: false,
        volume: 50,
      }
    },
    watch: {
      volume() {
        this.audioFile.volume = this.volume / 100;
      }
    },
    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      this.selectedSound = this.soundIsInChosenField();
      let self = this;
      EventBus.$on('pause-music', (tryingToPause) => {
        this.pause = tryingToPause;
        if (self.soundIsInChosenField()) {
          tryingToPause ? self.pauseSound() : self.playSound();
        }
      });

      EventBus.$on('update-volume', ({from: oldVol, to: newVol}) => {
        if (self.selectedSound) {
          //get old local volume here
          self.previousVolume = self.audioFile.volume * 100;
          //set volume proportionally to global volume
          self.audioFile.volume = (newVol / oldVol) * self.audioFile.volume;
          this.volume = self.audioFile.volume * 100;
        }
      });

      EventBus.$on('mute-volume', (mute) => {
        if (self.selectedSound) {
          self.audioFile.volume = mute ? 0 : self.previousVolume / 100
        }
      });
      this.initializePresetSound();
    },
    methods: {
      soundIsInChosenField() {
        return this.soundPresets.indexOf(this.audio) > -1;
      },
      addSound() {
        this.selectedSound = true;
        this.soundPresets.push(this.audio);
        if (!(this.pause)) {
          this.playSound();
        }
        this.$parent.$parent.nowPlayingList.push(this.audio)
      },
      removeSound() {
        let index = this.soundPresets.indexOf(this.audio);
        this.soundPresets.splice(index, 1);
        this.pauseSound();
        let nowPlayingAudioIndex = this.$parent.$parent.nowPlayingList.indexOf(this.audio);
        this.$parent.$parent.nowPlayingList.splice(nowPlayingAudioIndex, 1);
      },
      pauseSound() {
        this.audioFile.pause();
      },
      playSound(volume) {
        if (volume) {
          this.volume = volume;
        }
        this.audioFile.volume = this.volume / 100;
        this.audioFile.play();
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
          // start off preset sounds at 100. Might need to move this at a later point to sound_presets.py
          this.playSound(100);
          this.$parent.$parent.nowPlayingList.push(this.audio);
        }
      }
    },
    beforeDestroy() {
      this.selectedSound = false;
      this.pauseSound();
    }
  }
</script>

