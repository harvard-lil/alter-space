<template>
  <div class="container">
    <light-levers></light-levers>
    <br/>
    <sound-with-toggles :soundPresets="soundPresets"></sound-with-toggles>

    <div class="row">
      <!-- TODO: visual? -->
    </div>

  </div>
</template>

<script>
  import axios from 'axios';
  import SoundWithToggles from "./SoundLevers";
  import LightLevers from "./LightLevers";

  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";

  export default {
    name: "Activity",
    components: {
      SoundWithToggles,
      LightLevers
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
