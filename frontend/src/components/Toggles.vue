<template>
  <div class="row">
    <Sounds :showToggles="showToggles"
            :soundPresets="soundPresets"></Sounds>
  </div>
</template>

<script>
  import Sounds from './Sounds'
  export default {
    name: "Toggles",
    components: {Sounds},
    props: ['soundPresets', 'lightPresets'],
    data() {
      return {
        showToggles: true,
      }
    },
  }
</script>
