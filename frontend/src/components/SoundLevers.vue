<template>
  <div class="row sound-levers">
    <div class="col-12">
      <table class="table title-shape" :class="$route.params.name">
        <svgicon icon="triangle-sound"
                 width="100%"
                 height="100%"
                 title="Sound Levers"
                 class="triangle"
                 :class="$route.params.name"
                 stroke="0">
        </svgicon>

      </table>
      <table class="table cell-table table-top" :class="$route.params.name">
        <tr>
          <td width="15%">
            <play-button></play-button>
          </td>
          <td width="85%">
            <sound-slider></sound-slider>
          </td>
        <tr/>
      </table>
      <table class="table cell-table table-bottom"
             :class="$route.params.name">
        <tr>
          <td width="30%">
            <div class="list-inline-item btn-sound-item"
                 v-for="type in soundTypes"
                 :key="type">

              <svgicon :icon="type"
                       width="60"
                       height="60"
                       :original="true"
                       class="btn-round"
                       @click="showList(type)"
                       stroke="0">
              </svgicon>
              <label>{{type}}</label>
            </div>
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
      <table class="table cell-table table-bottom"
             :class="$route.params.name"
             v-show="showingList">
        <tr>
          <th class="row">
            <div class="col-6">
              Select or deselect {{soundType}} tracks
            </div>
            <div class="col-6 text-right">
              <a>
                Back to main view
                <span class="btn-x"></span>
              </a>
            </div>
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
  import "./icons/nature";
  import "./icons/urban";
  import "./icons/abstract";
  import './icons/triangle-sound';

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
