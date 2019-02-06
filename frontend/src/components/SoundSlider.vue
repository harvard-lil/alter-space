<template>

  <div class="td col-8">
    <input type="range"
           class="volume-range"
           min="0"
           max="100"
           value="100"
           autocomplete="off"
           v-model.lazy.number="volume"/>
    <label class="volume-label">
      volume
    </label>


  </div>

</template>

<script>
  import EventBus from '../event-bus';
  import './icons/volume';

  export default {
    name: "sound-slider",
    components: {},
    watch: {
      volume() {
        EventBus.$emit('update-volume', this.volume);
      }
    },
    data() {
      return {
        audio: undefined,
        volume: 100,
      }
    }
  }
</script>
<style scoped></style>
