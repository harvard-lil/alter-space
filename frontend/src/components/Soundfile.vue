<template>
  <div>
    <button @click="toggleButton" class="toggle" v-bind:class="{ on: toggle }">
      {{ audio }}
    </button>
    <!-- audio files are hidden from DOM / view -->
    <audio loop controls>
      <source :id="audio" :src="`${audioBaseUrl}/${audio}`" type="audio/mpeg">
    </audio>
  </div>
</template>

<script>
  const audioBaseUrl = process.env.BASE_URL + "sounds";

  export default {
    props: ['audio'],
    name: "soundfile",
    data() {
      return {
        audioBaseUrl: audioBaseUrl,
        toggle: false
      }
    },

    mounted() {
      this.audioFile = this.$el.querySelectorAll('audio')[0];
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
  }

  .toggle.on {
    background-color: navy;
  }
</style>
