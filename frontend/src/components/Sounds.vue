<template>
  <div class="sound-preset-container">

    <button @click="showList()"
            :class="{active: showList}"
            class="btn btn-default btn-sound-list btn-round">
      {{soundType}}
    </button>

    <ul class="sound-list" :class="{show: showingList}">
      <li v-for="audio in allSoundsOfType" :key="audio">
        <soundfile :audio="audio"
                   :soundType="soundType"
                   :showToggles="showToggles">
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
    props: ['showToggles', 'soundType', 'soundPresets'],
    data() {
      return {
        baseUrl: process.env.BASE_URL,
        showingList: false,
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
    mounted() {
      let self = this;
      /* collapse all other lists */
      this.$parent.$on("sounds-collapse-list", function (soundType) {
        if (soundType !== self.soundType) {
          self.showingList = false;
        }
      })
    },
    methods: {
      showList() {
        if (this.showingList) {
          this.showingList = false;
        } else {
          this.showingList = true;
          this.$parent.$emit("sounds-collapse-list", this.soundType);
        }
      }
    }
  }
</script>
