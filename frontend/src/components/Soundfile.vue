<template>
  <div :selectedSound="selectedSound"
       :audio="audio">
    <button @click="toggleButton()"
            class="btn-toggle btn-sound-add"
            v-bind:class="{ on: selectedSound }">
      {{ audioName }}
    </button>
    <br/>
    <!-- audio files are hidden from DOM / view -->
    <audio loop controls :preload="soundIsInChosenField() ? 'auto' : 'metadata'">
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
        pause: true,
        soundPresets: this.$parent.soundPresets,
        volume: 50,
        loadSoundEvent: this.$parent.$parent.loadSoundEvent
      }
    },
    watch: {
      volume() {
        this.audioFile.volume = this.volume / 100;
      }
    },
    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      this.audioFile.addEventListener(this.loadSoundEvent, this.soundLoaded, false);
      this.selectedSound = this.soundIsInChosenField();

      let self = this;
      EventBus.$on('play-music', (tryingToPlay) => {
        this.pause = !tryingToPlay;
        if (self.soundIsInChosenField()) {
          tryingToPlay ? self.playSound() : self.pauseSound();
        }
      });

      EventBus.$on('update-volume', ({from: oldVol, to: newVol}) => {
        if (self.selectedSound) {
          //get old local volume here
          self.previousVolume = self.audioFile.volume * 100;
          //set volume proportionally to global volume
          let newAudioVol = (newVol / oldVol) * self.audioFile.volume;
          if (newAudioVol > 1) {
            newAudioVol = 1
          }
          self.audioFile.volume = newAudioVol;
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
        if (this.soundPresets) {
          return Object.keys(this.soundPresets).indexOf(this.audio) > -1;
        }
      },
      addSound() {
        this.selectedSound = true;
        this.soundPresets[this.audio] = this.volume;
        if (!(this.pause)) {
          this.playSound();
        }
        this.$parent.$parent.nowPlayingList.push(this.audio)
      },
      removeSound() {
        delete this.soundPresets[this.audio];
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
      soundLoaded() {
        EventBus.$emit('sound-loaded', this.audio);
      },
      initializePresetSound() {
        // Plays sound if it's in the presets
        if (this.soundIsInChosenField()) {
          this.selectedSound = true;
          // start off preset sounds at 100. Might need to move this at a later point to sound_presets.py
          this.volume = this.soundPresets[this.audio];
          // this.playSound(this.volume);
          this.$parent.$parent.nowPlayingList.push(this.audio);
        }
      }
    },
    beforeDestroy() {
      this.selectedSound = false;
      this.removeSound();
    }
  }
</script>

