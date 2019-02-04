<template>
  <div class="container-preset row"
       :class="'activity-'+$route.params.name">
    <div class="col-centered text-center">
      <h1>
        {{translation[$route.params.name]}}
      </h1>
      <router-link
              :to="{ path: '/activity/' + $route.params.name}">

        <button class="btn btn-customize">
          Customize!
        </button>
      </router-link>
    </div>
  </div>
</template>

<script>
  // import axios from 'axios';
  const activityUrl = process.env.VUE_APP_BACKEND_URL + "activity/";

  export default {
    name: "preset",
    props: ["translation"],
    data() {
      return {}
    },
    beforeMount() {
      console.log("preset.vue: hello!")
    }
  }

</script>
