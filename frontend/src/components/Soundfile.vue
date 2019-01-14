<template>
  <div>
    <button @click="toggleButton" class="toggle" v-bind:class="{ on: toggle }">
      {{ audioName }}
    </button>
    <!-- audio files are hidden from DOM / view -->
    <audio loop controls>
      <source :id="audio" :play="play" :src="`${audio}`" type="audio/mpeg">
    </audio>
  </div>
</template>

<script>
  const audioBaseUrl = process.env.VUE_APP_BACKEND_URL + "sounds";
  function getAudioName(audioPath) {
    let parts = audioPath.split('/');
    return parts[parts.length - 1]
  }
  export default {
    props: ['audio', 'play'],
    name: "soundfile",
    data() {
      return {
        audioBaseUrl: audioBaseUrl,
        toggle: false,
        audioName: getAudioName(this.audio)
      }
    },

    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
      if (this.play) {
        this.toggleButton();
      }
    },

    methods: {
      toggleButton() {
        this.toggle = !this.toggle;
        this.toggle ? this.audioFile.play() : this.audioFile.pause();
      }
    }
  }
</script>

<style scoped>
  audio {
    display: none;
  }

  .toggle {
    background-color: blue;
    color: white;
    padding: 10px;
    margin: 0 0 20px 0;
    width: 150px;
    cursor: pointer;
    font-weight: 300;
    border: 0;
    border-radius: 5px;
  }

  .toggle.on {
    background-color: navy;
  }
</style>
