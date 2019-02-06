<template>
  <div class="col-centered col-3">
    Using light with id: <b>{{light}}</b>
  </div>
</template>

<script>
  export default {
    name: "Lights",
    data() {
      return {
        light: ""
      }
    },
    mounted() {
      if (this.$route.params.id) {
        localStorage.setItem('light', this.$route.params.id);
        this.light = this.$route.params.id;
      } else {
        this.light = localStorage.getItem('light');
      }
    }
  }
</script>
