<template>
  <div class="sound-preset-container">
    <button @click="showList()"
            :class="{active: showList}"
            class="btn btn-default btn-sound-list">
      {{soundType}}
    </button>

    <ul class="sound-list" :class="{show: showingList}">
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
        showingList: false,
        soundNames: []
      }
    },
    mounted() {
      let self = this;
      /* collapse all other lists */
      this.$parent.$on("sounds-collapse-list", function(soundType) {
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
