<template>
  <div class="col-centered col-6">
    <div class="col-12 alert-warning">{{error}}</div>
    <br/>
    <ul class="btn-group list-inline">
      <li v-for="val in lights" class="list-inline-item" v-bind:key="val">
      <button class="btn btn-default btn-light-choice" @click="setLight(val)">
        {{val}}
      </button>
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    name: "Lights",
    data() {
      return {
        lights: ["1", "2"],
        light: "",
        error: ""
      }
    },
    methods: {
      setLight(val) {
        this.light = val;
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
          this.error = "Light is not set. Please set light first by clicking one of the options below."
        }
      }
    }
  }
</script>
