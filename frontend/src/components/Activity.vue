<template>
  <div class="row activity-row">
    <div class="container-preset" :class="'activity-'+$route.params.name" v-if="!(customizing)">
      <div class="preset-content text-center">
        <h1>
          {{translation[$route.params.name]}}
        </h1>
        <p>Enjoy our presets, or customize to fit your mood below.</p>
        <ul class="list-inline">
          <li class="list-inline-item">
            <loader v-if="loading && !loadedAudio"></loader>
            <svgicon :icon="play ? 'pause-sounds' : 'play-sounds'"
                     v-if="!loading || loadedAudio"
                     class="btn-round btn-preset"
                     :class="play ? 'pause-sounds' : 'play-sounds'"
                     width="60"
                     height="60"
                     stroke="0"
                     @click="playMusic()">

            </svgicon>
            <p v-if="play">play sounds</p>
            <p v-else>pause sounds</p>
          </li>
          &nbsp;
          <li class="list-inline-item">
            <svgicon icon="customize-sliders"
                     class="btn-round btn-preset"
                     width="60"
                     height="60"
                     stroke="0"
                     @click="toggleCustomizing()">

            </svgicon>
            <p>customize!</p>
          </li>

        </ul>

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
                      :effectOn="effectOn"
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


  import './icons/play-sounds';
  import './icons/pause-sounds';
  import './icons/customize-sliders';

  import EventBus from '../event-bus';
  import SoundLevers from "./SoundLevers";
  import LightLevers from "./LightLevers";
  import Loader from "./Loader";

  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";

  export default {
    name: "Activity",
    components: {
      SoundLevers,
      LightLevers,
      Loader
    },
    data() {
      return {
        activity: this.$route.params.name,
        soundPresets: [],
        lightPresets: {},
        showingLightOptions: false,
        showingSoundOptions: false,
        taskID: "",
        loading: false,
        effect: "",
        customizing: false, // if this is set to true we skip the presets page and go straight to the customizing page
        effectOn: "",
        loadedAudio: false,
        play: false,
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
        this.stopEffectTask(() => {
          window.location.reload();
        });
      },
      stopEffectTask(cb) {
        let self = this;
        if (self.taskID && self.effect) {
          let url = process.env.VUE_APP_BACKEND_URL + "lights/effects/" + this.effect;
          let light = localStorage.getItem('light');
          let data = {
            id: light,
            effect: self.effect,
            task_id: self.taskID
          };
          axios({
            url: url,
            method: "post",
            data: data
          }).then((res) => {
            self.taskID = res.data.task_id;
            self.$parent.$parent.taskID = self.taskID;
            self.$parent.effectPlaying = self.breathe;
            cb();
          });
        } else {
          cb();
        }
      },
      playMusic() {
        let self = this;
        self.play = !self.play;
        if (self.play) {
          self.loading = true;
        }
        EventBus.$emit('play-music', self.play)
      },
      getPresets() {
        let url = activityUrl + this.$route.params.name;
        let self = this;
        axios.get(url)
            .then((res) => {
              self.soundPresets = res.data.sound;
              self.lightPresets = res.data.light;
              self.effectOn = self.lightPresets.effect
            });

      },
    },
    beforeMount() {
      this.getPresets();
      let self = this;
      EventBus.$on('sound-loaded', () => {
        self.loading = false;
        self.loadedAudio = true;
      })
    },
    beforeRouteLeave(to, from, next) {
      // disable chasing and breathing effects
      this.notCustomizing();
      if (!(this.effect)) {
        this.effect = "breathe";
      }
      this.stopEffectTask(() => {
        next();
      })
    },

  }

</script>
