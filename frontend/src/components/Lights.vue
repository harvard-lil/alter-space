<template>
  <div class="col-centered col-6">
    <div class="col-12 alert-warning">{{error}}</div>
    <span class="text-center">
      Using light with id: <b>{{light}}</b>
    </span>
  </div>
</template>

<script>
  export default {
    name: "Lights",
    data() {
      return {
        light: "",
        error: ""
      }
    },
    mounted() {
      if (this.$route.params.id) {
        localStorage.setItem('light', this.$route.params.id);
        this.light = this.$route.params.id;
      } else {
        this.light = localStorage.getItem('light');
        if (!(this.light)) {
          this.error = "Light is not set. Please set light first by going to /light/your-light-id"
        }
      }
    }
  }
</script>
