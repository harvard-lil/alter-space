<template>
  <ul>
    <li v-for="audio in audioPaths" :key="audio">
      <soundfile :audio="audio" :play="play" :showToggles="showToggles"></soundfile>
    </li>
  </ul>
</template>

<script>
  import axios from 'axios';
  import soundfile from './Soundfile'

  const audioBaseUrl = process.env.VUE_APP_BACKEND_URL + "sounds";

  export default {
    name: "Sounds",
    components: {
      soundfile
    },
    props: ['showToggles', 'soundPresets'],
    data() {
      return {
        baseUrl: process.env.BASE_URL,
        audioPaths: [],
        play: false
      }
    },
    mounted() {
    },
    methods: {
      getFiles() {
        axios.get(audioBaseUrl)
            .then((res) => {
              this.filterChosenSounds(res.data);
            })
      },
      filterChosenSounds(allSounds) {
        if (this.soundPresets && this.soundPresets.length) {
          for (let i = 0; i < this.soundPresets.length; i++) {
            this.audioPaths.push(allSounds[this.soundPresets[i]]);
          }
          // And then, play all the chosen sounds
          this.play = true;
        } else {
          this.audioPaths = allSounds;
        }
      }
    },
    created() {
      this.getFiles()
    }
  }
</script>

<style>
  ul {
    list-style: none;
  }
</style>