<template>
  <div class="row">
    <Sounds :showToggles="showToggles"
            :soundPresets="soundPresets">
    </Sounds>
  </div>

</template>

<script>

  import Sounds from './Sounds'

  export default {
    name: "sound-with-toggles",
    components: {Sounds},
    props: ['soundPresets'],
    data() {
      return {
        showToggles: true,
      }
    },
  }

</script>
