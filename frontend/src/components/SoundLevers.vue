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
    <div class="table cell-table table-top-single " :class="[$route.params.name, {expanded: showingList, 'table-top': showingList}]">
      <div class="tr">
        <play-button></play-button>
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
            <label v-if="type === 'abstract' ">tone</label>
            <label v-else>{{type}}</label>
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
      <div class="tr sound-type-container"
           :class="type"
           v-for="type in soundTypes"
           v-bind:key="type"
           v-show="type === soundType">
        <svgicon icon="arrow-up"
                 class="arrow-up"
                 :class="type">
        </svgicon>
        <Sounds :soundPresets="soundPresets[type]"
                :soundType="type">
        </Sounds>
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
  import './icons/arrow-up';

  import PlayButton from './PlayButton'
  import Sounds from './Sounds'

  export default {
    name: "sound-levers",
    components: {
      Sounds,
      PlayButton
    },
    props: ["soundPresets", "collapseSoundOptions"],
    data() {
      return {
        showToggles: true,
        soundTypes: ['nature', 'urban', 'abstract'],
        soundType: "",
        showingList: false,
        chosenSounds: [],
        nowPlayingList: [],
        showMaxPlaying: 3,
        userAgent: "", // see getUserAgent for explanation
        loadSoundEvent: "canplay" // versus canplaythrough. ios needs the latter, everything else needs the former
      }
    },
    beforeMount() {
      this.setPreloadSoundEvent();
    },
    mounted() {
      let self = this;
      /* collapse all other lists */
      this.$on("sounds-collapse-list", function (soundType) {
        if (soundType !== self.soundType) {
          self.showingList = false;
        }
      });
    },
    watch: {
      collapseSoundOptions() {
        if (this.collapseSoundOptions) {
          this.showingList = false;
          this.$parent.showingSoundOptions = false;
        }
      }
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
        this.$parent.showingSoundOptions = true;
      },
      getUserAgent() {
        /* This is necessary because the world is terrible and unfair.
        *  iOS devices that rely on mobile data don't allow any sort of preloading of audio files.
        *  They require physical triggering (like a button press) to start loading the files.
        *  For a final cherry on top, they also don't seem to buffer the media -- they wait until the audio is fully
        *  loaded before playing. On any device other than iOSes, we can rely on the "canplay" event. On iOSes, we must rely on "canplaythrough". */
        this.userAgent = navigator.userAgent;
      },
      setPreloadSoundEvent() {
        this.getUserAgent();
        let forbiddenDevices = ["iPad", "iPhone", "iPod"];
        for (let i = 0; i < forbiddenDevices.length; i++) {
          if (this.userAgent.indexOf(forbiddenDevices[i]) > -1) {
            this.loadSoundEvent = "canplaythrough";
            return
          }
        }
      }
    },
  }

</script>
