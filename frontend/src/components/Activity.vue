<template>
  <div class="container">

    <div class="row">
      <div class="col-12">
        <h1>{{activity}}</h1>
      </div>
      <div class="col-12">
        <p>Playing now...</p>
      </div>
    </div>
    <sound-with-toggles :soundPresets="soundPresets">

    </sound-with-toggles>

    <br/><hr/><br/>
      <div class="row">
    <div class="col-12">
      <h1>All options</h1>
    </div>
    <div class="col-6">
      <h4>Lights</h4>
      <Lights></Lights>
    </div>
    <div class="col-6">
      <h4>Sounds</h4>
      <Sounds></Sounds>
    </div>
      </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import SoundWithToggles from "./SoundWithToggles";
  import Sounds from './Sounds';
  import Lights from './Lights';

  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";

  export default {
    name: "Activity",
    components: {
      Sounds,
      Lights,
      SoundWithToggles},
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
