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
            <ul v-for="sound in sounds"
                v-bind:key="sound">
              <li>{{sound}}</li>
            </ul>
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

  function getAudioName(audioPath) {
    let parts = audioPath.split('/');
    return parts[parts.length - 1]
  }


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
        sounds: [],
        presetsNature: [],
        presetsUrban: [],
        presetsAbstract: [],
        allSoundPresets: [],
        mute: "Mute",
      }
    },
    mounted() {
      let self = this;
      EventBus.$on('mute-volume', function(mute){
        self.mute = mute ? "Unmute" : "Mute";
      });
    },
    beforeCreate() {
      /* TODO: name sounds like nature_sound-name and urban_sound-name.
        * Sort here. For now, sort randomly */
      axios.get(audioBaseUrl)
          .then((res) => {
            this.allSoundPresets = res.data;
            this.presetsNature = this.allSoundPresets.slice(5, 9);
            this.presetsUrban = this.allSoundPresets.slice(0, 5);
            this.presetsAbstract = this.allSoundPresets.slice(6, 8);
            let chosenSounds = this.$parent.soundPresets;
            for (let i = 0; i < chosenSounds.length; i++) {
              let name = getAudioName(this.allSoundPresets[chosenSounds[i]]);
              this.sounds.push(name)
            }
          })

    }
  }

</script>
<style scoped>
  .table-1 {
    -moz-box-shadow: 1px 0 5px rgba(0, 0, 0, 0.2);
    -webkit-box-shadow: 1px 0 5px rgba(0, 0, 0, 0.2);
    box-shadow: 1px 0 5px rgba(0, 0, 0, 0.2);
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