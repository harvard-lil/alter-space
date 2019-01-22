<template>
  <div class="container">

    <div class="row">
      <div class="col-12">
        <h1>{{activity}}</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-4">
        <sound-with-toggles :soundPresets="soundPresets">
        </sound-with-toggles>
      </div>
      <div class="col-4">
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
  import Sounds from './Sounds';
  import Lights from './Lights';

  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";

  export default {
    name: "Activity",
    components: {
      Sounds,
      Lights,
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
    methods: {
      getPresets() {
        axios.get(activityUrl + this.activity)
            .then((res) => {
              this.soundPresets = res.data.sound;
              this.lightPresets = res.data.light;
            })
      },
    },
    created() {
       this.getPresets()
    }
  }

</script>
