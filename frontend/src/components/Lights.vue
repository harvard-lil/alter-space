<template>
  <div class="col-centered col-6">
    <div class="col-12 alert-warning">{{error}}</div>
    <form>
    <span class="text-center">
      // TODO: fix this for future iterations, we shouldn't need to hardcode max and min like this
      Using light with id: <input title="light"
                                  type="number"
                                  max="2"
                                  min="1"
                                  v-model="light">
    </span>
      <button type="submit" @click="setLight">Submit</button>
    </form>
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
    methods: {
      setLight() {
        localStorage.setItem('light', this.light);
        this.$router.replace('/');
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
