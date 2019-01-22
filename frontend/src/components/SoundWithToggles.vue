<template>

  <div class="row">
    <play-button></play-button>
    <h3>Now playing:</h3>
    <ul>
      <li></li>
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

  export default {
    name: "sound-with-toggles",
    components: {Sounds, PlayButton},
    props: ['soundPresets'],

    data() {
      return {
        showToggles: true,
        pause: false,
      }
    },
  }

</script>
