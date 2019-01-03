<template>
  <ul>
    <li v-for="audio in audioFiles" :key="audio">
      <soundfile :audio="audio"></soundfile>
    </li>
  </ul>
</template>

<script>
  import axios from 'axios';
  import soundfile from './Soundfile'

  const audioBaseUrl = process.env.BASE_URL + "sounds";

  export default {
    name: "Sounds",
    components: {
      soundfile
    },
    data() {
      return {
        baseUrl: process.env.BASE_URL,
        audioBaseUrl: audioBaseUrl,
        audioFiles: []
      }
    },
    mounted() {
      console.log(this.audioFiles)
    },

    methods: {
      getFiles() {
        axios.get(audioBaseUrl)
            .then((res) => {
              this.audioFiles = res.data
              console.log(this.audioFiles)
            })
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