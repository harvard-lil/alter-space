<template>
  <div class="row">
    <div class="col-12 gray-bar">
      <ul class="list-inline">
        <li class="list-inline-item">
          <h3 class="settings-title">Settings</h3>
        </li>
        <li class="list-inline-item">
          <button class="float-right">Reset</button>
        </li>
      </ul>


    </div>
    <div class="lever-container col-centered">
      <light-levers class="color-levers"></light-levers>
      <br/>
      <sound-levers :soundPresets="soundPresets"></sound-levers>

      <div class="row">
        <!-- TODO: visual? -->
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import SoundLevers from "./SoundLevers";
  import LightLevers from "./LightLevers";

  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";

  export default {
    name: "Activity",
    components: {
      SoundLevers,
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
