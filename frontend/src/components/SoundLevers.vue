<template>
  <div class="row sound-levers">
    <div class="col-12">
      <h3>Sounds</h3>
    </div>
    <div class="col-12">
      <table class="table cell-table table-1">
        <tr>
          <td>
            <play-button></play-button>
            <label>Play</label>
            <!--TODO: play or pause-->
          </td>
          <td>
            <!--TODO: mute button-->
            <sound-slider></sound-slider>
            <label>{{ mute }}</label>
            <label class="volume-label">
              Volume
            </label>
          </td>
        <tr/>
      </table>
      <table class="table cell-table table-2">
        <tr>
          <td>
            <ul>
              <li>
                <Sounds :showToggles="showToggles"
                        :soundPresets="presetsNature"
                        :soundType="'nature'">
                </Sounds>
              </li>
              <li>
                <Sounds :showToggles="showToggles"
                        :soundPresets="presetsUrban"
                        :soundType="'urban'">
                </Sounds>
              </li>
              <li>
                <Sounds :showToggles="showToggles"
                        :soundPresets="presetsAbstract"
                        :soundType="'abstract'">
                </Sounds>
              </li>
            </ul>
          </td>
          <td colspan="15">
            <h3>Now playing:</h3>
            <div v-for="val in sounds" :key="val">
              <ul v-for="sound in val" :key="sound">
                <li>
                  {{getAudioName(sound)}}
                </li>
              </ul>
            </div>
          </td>
        </tr>
      </table>
    </div>
  </div>

</template>

<script>

  import axios from 'axios';
  import EventBus from '../event-bus'

  import PlayButton from './PlayButton'
  import SoundSlider from './SoundSlider'
  import Sounds from './Sounds'
  const audioBaseUrl = process.env.VUE_APP_BACKEND_URL + "sounds";

  export default {
    name: "sound-with-toggles",
    components: {
      SoundSlider,
      Sounds,
      PlayButton
    },
    props: ['soundPresets'],
    data() {
      return {
        showToggles: true,
        pause: false,
        sounds: {},
        presetsNature: [],
        presetsUrban: [],
        presetsAbstract: [],
        allSoundPresets: [],
        mute: "Mute",
      }
    },
    mounted() {
      let self = this;
      EventBus.$on('mute-volume', function (mute) {
        self.mute = mute ? "Unmute" : "Mute";
      });
    },
    methods: {
      getAudioName(audioPath) {
        let name = audioPath.split(".mp3")[0];
        let parts = name.split('_');
        return parts.join(" ");
      },

    },

    beforeCreate() {
      let self = this;
      axios.get(audioBaseUrl)
          .then((res) => {
            self.allSoundPresets = res.data;
            self.presetsNature = self.allSoundPresets.nature;
            self.presetsUrban = self.allSoundPresets.urban;
            self.presetsAbstract = self.allSoundPresets.abstract;
            self.sounds = self.$parent.soundPresets;
          })
    }
  }

</script>

<style scoped>
  /* Extra styles because of tables stacked */
  .table-1 {
    -moz-box-shadow: 1px 0 5px rgba(230, 230, 230, 0.8);
    -webkit-box-shadow: 1px 0 5px rgba(230, 230, 230, 0.8);
    box-shadow: 1px 0 5px rgba(230, 230, 230, 0.8);
    height: 125px;
  }

  .table-1 label {
    bottom: auto;
  }

  .table-1 label.volume-label {
    margin-left: 30%;
  }

  .table-2 {
    border-top: 0;
  }

</style>