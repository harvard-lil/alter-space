<template>

  <div class="row">
    <play-button></play-button>
    <sound-slider></sound-slider>
    <h3>Now playing:</h3>
    <ul v-for="sound in sounds">
      <li>{{sound}}</li>
    </ul>
    <Sounds :showToggles="showToggles"
            :soundPresets="naturePresets"
            :type="nature">
    </Sounds>

  </div>

</template>

<script>

  import Sounds from './Sounds'
  import PlayButton from './PlayButton'
  import SoundSlider from './SoundSlider'

  export default {
    name: "sound-with-toggles",
    components: {
      SoundSlider,
      Sounds,
      PlayButton},
    props: ['soundPresets'],

    data() {
      return {
        showToggles: true,
        pause: false,
        sounds: this.$parent.soundPresets
      }
    },
  }

</script>
