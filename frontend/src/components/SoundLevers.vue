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
            <ul class="list-inline">
              <li class="list-inline-item">
                <Sounds :showToggles="showToggles"
                        :soundPresets="presetsNature"
                        :soundType="'nature'">
                </Sounds>
              </li>
              <li class="list-inline-item">
                <Sounds :showToggles="showToggles"
                        :soundPresets="presetsUrban"
                        :soundType="'urban'">
                </Sounds>
              </li>
              <li class="list-inline-item">
                <Sounds :showToggles="showToggles"
                        :soundPresets="presetsAbstract"
                        :soundType="'abstract'">
                </Sounds>
              </li>
            </ul>
          </td>
          <!--Now playing container -->
          <td colspan="15" class="now-playing-container">
            <span>Now playing:</span>
            <div class="soundtype-container"
                 v-for="val in soundPresets"
                 :key="val">
              <ul class="list-inline"
                  v-for="sound in val"
                  :key="sound">
                <li class="list-inline-item">
                  {{getAudioName(sound)}}
                </li>
              </ul>
            </div>
          </td>
        </tr>
      </table>
      <table class="table cell-table table-2">
      </table>
    </div>
  </div>

</template>

<script>

  import EventBus from '../event-bus'

  import PlayButton from './PlayButton'
  import SoundSlider from './SoundSlider'
  import Sounds from './Sounds'

  export default {
    name: "sound-levers",
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
        mute: "Mute",
        presetsNature: [],
        presetsUrban: [],
        presetsAbstract: []
      }
    },
    mounted() {
      let self = this;
      EventBus.$on('mute-volume', function (mute) {
        self.mute = mute ? "Unmute" : "Mute";
      });
      this.presetsNature = this.soundPresets["nature"];
      this.presetsUrban =  this.soundPresets["urban"];
      this.presetsAbstract = this.soundPresets["abstract"];
    },
    methods: {
      getAudioName(audioPath) {
        let name = audioPath.split(".mp3")[0];
        let parts = name.split('_');
        return parts.join(" ");
      },

    },
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