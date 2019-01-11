<template>
  <div class="container">

    <div class="row">
      <div class="col-12">
        <h1>{{activity}}</h1>
      </div>
      <div class="col-12">
        <p>Playing now...</p>
      </div>
    </div>
    <br/><br/><br/><br/>
    <div class="row">
      <div class="col-6">
        <h4>Lights</h4>
        <Lights></Lights>
      </div>
      <div class="col-6">
        <h4>Sounds</h4>
        <Sounds></Sounds>
      </div>
    </div>
  </div>
</template>

<script>
  import Sounds from './Sounds'
  import Lights from './Lights'

  export default {
    name: "Activity",
    props: ["name"],
    components: {Lights, Sounds},
    mounted() {
      window.route = this.$route
    },
    data() {
      return {
        activity: this.$route.query.name
      }
    },
  }

</script>

<style scoped>
  h1 {
    text-transform: uppercase;
  }

</style>