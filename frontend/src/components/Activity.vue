<template>
  <div class="container">

    <div class="row">
      <div class="col-12">
        <h1>{{activity}}</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-4">
        <h3>Sounds</h3>
        <sound-with-toggles :soundPresets="soundPresets">
        </sound-with-toggles>
      </div>
      <div class="col-4">
        <h3>Lights</h3>
        <light-with-toggles>
        </light-with-toggles>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import SoundWithToggles from "./SoundWithToggles";
  import LightWithToggles from "./LightWithToggles";

  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";

  export default {
    name: "Activity",
    components: {
      SoundWithToggles,
      LightWithToggles
    },
    data() {
      return {
        activity: this.$route.query.name,
        soundPresets: [],
        lightPresets: [],
      }
    },
    beforeCreate() {
      let url = activityUrl + this.$route.query.name;
      axios.get(url)
          .then((res) => {
            this.soundPresets = res.data.sound;
            this.lightPresets = res.data.light;
          })
    },


  }

</script>
