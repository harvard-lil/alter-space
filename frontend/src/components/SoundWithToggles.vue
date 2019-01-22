<template>
  <div class="row">

    <play-button></play-button>
    <Sounds :showToggles="showToggles"
            :soundPresets="soundPresets">
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
      }
    },
  }

</script>
