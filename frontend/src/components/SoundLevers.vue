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
              <li class="list-inline-item"
                  v-for="type in soundTypes"
                  :key="type">
                <button @click="showList(type)"
                        :class="{active: type === soundType}"
                        class="btn btn-default btn-sound-list btn-round">
                  {{type}}
                </button>

              </li>
            </ul>
          </td>
          <!--Now playing container -->
          <td colspan="15" class="now-playing-container">
            <span>Now playing:</span>
            <div class="soundtype-container"
                 v-for="soundType in soundTypes"
                 :key="soundType">
              <ul class="list-inline"
                  v-for="sound in soundPresets[soundType]"
                  :key="sound">
                <li class="list-inline-item">
                  {{getAudioName(sound)}}
                </li>
              </ul>
            </div>
          </td>
        </tr>
      </table>
      <table class="table cell-table table-2"
             v-show="showingList">
        <tr>
          <th>
            Select or deselect {{soundType}} tracks
          </th>
        </tr>
        <tr>
          <div v-for="type in soundTypes"
               v-bind:key="type"
               v-show="type === soundType">
            <Sounds :soundPresets="soundPresets[type]"
                    :soundType="type">
            </Sounds>

          </div>
        </tr>
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
        soundTypes: ['nature', 'urban', 'abstract'],
        soundType: "",
        showingList: false,
      }
    },
    mounted() {
      let self = this;
      EventBus.$on('mute-volume', function (mute) {
        self.mute = mute ? "Unmute" : "Mute";
      });

      /* collapse all other lists */
      this.$on("sounds-collapse-list", function (soundType) {
        if (soundType !== self.soundType) {
          self.showingList = false;
        }
      })

    },
    methods: {
      getAudioName(audioPath) {
        let name = audioPath.split(".mp3")[0];
        let parts = name.split('_');
        return parts.join(" ");
      },
      showList(soundType) {
        if (this.showingList && soundType === this.soundType) {
          this.showingList = false;
          this.soundType = "";
        } else {
          this.soundType = soundType;
          this.showingList = true;
          this.$emit("sounds-collapse-list", this.soundType);
        }
      }
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