<template>
  <div class="row activity-row">
    <div class="container-preset" :class="'activity-'+$route.params.name" v-if="!(customizing)">
      <div class="preset-content text-center">
        <h1>
          {{translation[$route.params.name]}}
        </h1>

        <button class="btn btn-customize"
                @click="toggleCustomizing()"
                :class="$route.params.name">
          Customize!
        </button>
      </div>
    </div>
    <div class="activity-container" v-show="customizing">
      <div class="activity row">

        <button @click="resetActivity()"
                class="btn btn-reset">
          Reset
        </button>

      </div>
      <div class="lever-container col-centered">
        <light-levers :lightPresets="lightPresets"
                      :collapseLightOptions="showingSoundOptions"
                      class="color-levers">
        </light-levers>
        <!--including space when not showing light options-->
        <div v-show="!showingLightOptions"><br/><br/><br/></div>

        <sound-levers :soundPresets="soundPresets"
                      :collapseSoundOptions="showingLightOptions"
                      :class="{fillbackground: showingLightOptions}">
        </sound-levers>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import EventBus from '../event-bus';
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
        taskID: "",
        effect: "",
        customizing: false,
        translation: {
          'relax': 'ReLaX',
          'read': 'READ',
          'focus': 'FOcUs',
          'create': 'cREATe',
          'meditate': 'mEdITAtE',
          'wyrd': 'W3!Rd',
        }
      }
    },
    methods: {
      toggleCustomizing() {
        this.customizing = !(this.customizing);
        EventBus.$emit('customizing', this.customizing);
      },
      notCustomizing() {
        this.customizing = false;
        EventBus.$emit('customizing', false);
      },
      resetActivity() {
        //TODO: use this.getPresets(): and make sure the sounds work
        window.location.reload();
      },
      getPresets() {
        let url = activityUrl + this.$route.params.name;
        let self = this;
        axios.get(url)
            .then((res) => {
              self.soundPresets = res.data.sound;
              self.lightPresets = res.data.light;
            });
      }
    },
    beforeMount() {
      this.getPresets();
    },
    beforeRouteLeave(to, from, next) {
      // disable chasing and breathing effects
      let self = this;
      self.notCustomizing();
      if (self.taskID && self.effect) {
        let url = process.env.VUE_APP_BACKEND_URL + "lights/effects/" + this.effect;
        let light = localStorage.getItem('light');
        let bodyFormData = new FormData();
        bodyFormData.set('id', light);
        bodyFormData.set('effect', self.effect);
        bodyFormData.set('task_id', self.taskID);

        axios({
          method: "post",
          url: url,
          data: bodyFormData
        }).then((res) => {
          self.taskID = res.data.task_id;
          self.$parent.$parent.taskID = self.taskID;
          self.$parent.effectPlaying = self.breathe;
        });
      }
      next()
    },

  }

</script>
