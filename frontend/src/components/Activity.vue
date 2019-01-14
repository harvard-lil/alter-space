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
    <Toggles :soundPresets="soundPresets" :lightPresets="lightPresets"></Toggles>
    <hr/>
    <Library></Library>
  </div>
</template>

<script>
  import axios from 'axios';
  import Toggles from './Toggles'
  import Library from './Library'

  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";
  
  export default {
    name: "Activity",
    components: {Library, Toggles},
    mounted() {

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
