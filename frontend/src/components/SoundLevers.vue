<template>
  <div class="row sound-levers">
    <div class="title-shape" :class="$route.params.name">
      <svgicon icon="triangle-sound"
               width="100%"
               height="auto"
               title="Sound Levers"
               class="triangle"
               :class="$route.params.name"
               stroke="0">
      </svgicon>

    </div>
    <div class="table cell-table table-top" :class="$route.params.name">
      <div class="tr">
        <play-button></play-button>
        <mute-button></mute-button>
        <sound-slider></sound-slider>
      </div>
    </div>
    <div class="table cell-table table-bottom"
         :class="[$route.params.name, {expanded: showingList}]">
      <div class="tr">
        <div class="td col-1 list-inline-item btn-sound-item"
             v-for="type in soundTypes"
             :key="type">

          <svgicon :icon="type"
                   width="60"
                   height="60"
                   :original="true"
                   class="btn-default"
                   @click="showList(type)"
                   stroke="0">
          </svgicon>
          <label>{{type}}</label>
        </div>
        <!--Now playing container -->
        <div class="col-1 td"></div>
        <div class="col-8 td now-playing-container text-left">
          <span>Now playing:</span>
          <div class="soundtype-container"
               v-for="soundType in soundTypes"
               :key="soundType">
            <ul class="list-inline">
              <li :key="sound"
                  v-for="sound in soundPresets[soundType]"
                  class="list-inline-item">
                {{getAudioName(sound)}}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="table cell-table table-bottom"
         :class="$route.params.name"
         v-show="showingList">
      <div class="tr row">
        <div class="col-6">
          Select or deselect {{soundType}} tracks
        </div>
        <div class="col-6 text-right">
          <a>
            Back to main view
            <span class="btn-x"></span>
          </a>
        </div>
      </div>
      <div class="tr">
        <div v-for="type in soundTypes"
             v-bind:key="type"
             v-show="type === soundType">
          <Sounds :soundPresets="soundPresets[type]"
                  :soundType="type">
          </Sounds>
        </div>
      </div>
    </div>
    <div class="title-shape"
         :class="$route.params.name"
         v-show="showingList">
      <svgicon icon="triangle-upside-down"
               width="100%"
               height="auto"
               title="Sound Levers"
               class="triangle"
               :class="$route.params.name"
               stroke="0">
      </svgicon>
    </div>
  </div>
</template>

<script>
  import "./icons/nature";
  import "./icons/urban";
  import "./icons/abstract";
  import './icons/triangle-sound';
  import './icons/triangle-upside-down';

  import PlayButton from './PlayButton'
  import MuteButton from './MuteButton'
  import SoundSlider from './SoundSlider'
  import Sounds from './Sounds'

  export default {
    name: "sound-levers",
    components: {
      SoundSlider,
      Sounds,
      PlayButton,
      MuteButton
    },
    props: ['soundPresets'],
    data() {
      return {
        showToggles: true,
        soundTypes: ['nature', 'urban', 'abstract'],
        soundType: "",
        showingList: false,
      }
    },
    mounted() {
      let self = this;
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
        let newName = parts.join(" ");
        // return newName += ',';
        return newName;
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
