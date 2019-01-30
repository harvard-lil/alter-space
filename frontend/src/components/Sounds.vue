<template>
  <div class="sound-preset-container">
    <ul class="sound-list list-inline">
      <li class="list-inline-item" v-for="audio in allSoundsOfType" :key="audio">
        <soundfile :audio="audio"
                   :soundType="soundType">
        </soundfile>

      </li>
    </ul>
  </div>
</template>

<script>
  import axios from 'axios';
  import soundfile from './Soundfile';
  const audioBaseUrl = process.env.VUE_APP_BACKEND_URL + "sounds";

  export default {
    name: "Sounds",
    components: {
      soundfile
    },
    props: ['soundType', 'soundPresets'],
    data() {
      return {
        baseUrl: process.env.BASE_URL,
        soundNames: [],
        allSoundsOfType: [],
      }
    },
    beforeMount() {
      let self = this;
      let url = audioBaseUrl + "/" + this.soundType;
      axios.get(url)
          .then((res) => {
            self.allSoundsOfType = res.data;
          })
    },
    methods: {
    }
  }
</script>
