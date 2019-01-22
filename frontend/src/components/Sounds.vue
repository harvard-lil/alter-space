<template>
  <div class="sound-preset-container">
    <button @click="showList = !showList"
            :class="{active: showList}"
            class="btn-sound-list">
      {{soundType}}
    </button>

    <ul class="sound-list" :class="{show: showList}">
      <li v-for="(audio, index) in soundPresets"
          :key="audio">
        <soundfile :audio="audio"
                   :index="index"
                   :showToggles="showToggles">
        </soundfile>

      </li>
    </ul>
  </div>
</template>

<script>
  import soundfile from './Soundfile'

  export default {
    name: "Sounds",
    components: {
      soundfile
    },
    props: ['showToggles', 'soundType', 'soundPresets'],
    data() {
      return {
        baseUrl: process.env.BASE_URL,
        showList: false,
        soundNames: []
      }
    },
  }
</script>
