<template>
  <div class="row">
    <!--{{$route}}-->
        <!--<router-link to="/preset">Go to Foo</router-link>-->
    <div class="gray-bar">
      <div class="col-12 col-centered">
        <ul class="list-inline">
          <li class="list-inline-item">
            <h5 class="settings-title">Settings</h5>
          </li>
          <li class="list-inline-item">
            <button @click="resetActivity()"
                    class="btn btn-reset">Reset</button>
          </li>
        </ul>
      </div>

    </div>
    <div class="lever-container col-centered">

      <light-levers class="color-levers"></light-levers>
      <br/><br/>
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
        activity: this.$route.params.name,
        soundPresets: [],
        lightPresets: [],
      }
    },
    methods: {
      resetActivity() {
        window.location.reload();
      }
    },
    beforeCreate() {
      let url = activityUrl + this.$route.params.name;
      axios.get(url)
          .then((res) => {
            this.soundPresets = res.data.sound;
            this.lightPresets = res.data.light;
          })
    },


  }

</script>
