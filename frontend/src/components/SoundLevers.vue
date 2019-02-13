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
        <div class="td btn-sound-container">
          <div class="list-inline-item btn-sound-item"
               v-for="type in soundTypes"
               :key="type">

            <svgicon :icon="type"
                     width="60"
                     height="60"
                     :original="true"
                     class="btn-default btn-sound-type"
                     :class="[type, {expanded: showingList && soundType === type }]"
                     @click="showList(type)"
                     stroke="0">
            </svgicon>
            <label>{{ type }}</label>
          </div>
        </div>
        <!--Now playing container -->
        <div class="td now-playing-container text-left">
          <span v-show="nowPlayingList.length">Now playing: </span>
          <div class="soundtype-container">
            <!-- Complicated logic to show sounds played until they get to be too long -->
            <!-- in that case, show all sounds until the 5th, then add "[+x]" -->
            <ul class="list-inline">
              <template v-if="nowPlayingList.length > 5">
                <li :key="sound"
                    v-for="(sound, key) in nowPlayingList.slice(0, 5)"
                    class="list-inline-item currently-playing-sound">
                  <template v-if="key >= 4">
                    [+{{nowPlayingList.length - 4}}]
                  </template>
                  <template v-else>
                    {{ getAudioName(sound) }},
                  </template>
                </li>

              </template>
              <template v-else>
                <li :key="sound"
                    v-for="(sound, key) in nowPlayingList"
                    class="list-inline-item currently-playing-sound">
                  <template v-if="nowPlayingList.length-1 === key ">
                    {{ getAudioName(sound) }}
                  </template>
                  <template v-else>
                    {{ getAudioName(sound) }},
                  </template>
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="table cell-table table-bottom"
         :class="$route.params.name"
         v-show="showingList">
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
        chosenSounds: [],
        nowPlayingList: [],
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
