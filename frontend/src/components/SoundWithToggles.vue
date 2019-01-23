<template>

  <div class="row">
    <play-button></play-button>
    <sound-slider></sound-slider>
    <h3>Now playing:</h3>
    <ul v-for="sound in sounds"
        v-bind:key="sound">
      <li>{{sound}}</li>
    </ul>
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

  </div>

</template>

<script>

  import axios from 'axios';

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
        allSoundPresets: []
      }
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
