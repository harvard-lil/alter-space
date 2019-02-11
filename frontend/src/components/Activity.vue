<template>
  <div class="row activity-row">
    <div class="row">
      <button @click="resetActivity()"
              class="btn btn-reset">Reset
      </button>
    </div>
    <div class="lever-container col-centered">
      <light-levers :lightPresets="lightPresets"
                    class="color-levers">
      </light-levers>
      <div v-show="!showingLightOptions">
        <br/><br/><br/>
      </div>
      <sound-levers :soundPresets="soundPresets"
                    :class="{fillbackground: showingLightOptions}"></sound-levers>
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
        lightPresets: {},
        showingLightOptions: false,
        showingSoundOptions: false,
      }
    },
    methods: {
      resetActivity() {
        window.location.reload();
      }
    },
    beforeMount() {
      let url = activityUrl + this.$route.params.name;
      let self = this;
      axios.get(url)
          .then((res) => {
            self.soundPresets = res.data.sound;
            self.lightPresets = res.data.light;
          });
    },
  }

</script>
