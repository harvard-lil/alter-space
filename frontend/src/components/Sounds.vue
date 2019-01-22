<template>
  <ul>
    <li v-for="(audio, index) in audioPaths" :key="audio">
      <soundfile :audio="audio"
                 :index="index"
                 :globalPause="globalPause"
                 :showToggles="showToggles">
      </soundfile>

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
    props: ['showToggles'],
    data() {
      return {
        baseUrl: process.env.BASE_URL,
        audioPaths: [],
        globalPause: false
      }
    },
    mounted() {
    },
    methods: {
      getFiles() {
        axios.get(audioBaseUrl)
            .then((res) => {
              this.audioPaths = res.data;
              // if soundPresets exist, filter list
              // otherwise, show everything
            })
      },
    },

    created() {
      this.getFiles();
      // EventBus.$on("pause-music", function (pause) {
      //   this.globalPause = pause;
      // })
    }
  }
</script>
