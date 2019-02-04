<template>
  <div class="container-preset row"
       :class="'activity-'+$route.params.name">
    <ul class="nav" :class="'activity-'+$route.params.name">
      <li class="nav-item col-2">
        <div class="button-label-container">
          <a href="/">
            <svgicon icon="home"
                     width="60"
                     height="60"
                     :original="true"
                     class="btn-round"
                     stroke="0"></svgicon>
            Home</a>
        </div>
      </li>
      <li class="nav-item col-2">
        <div class="button-label-container">
          <svgicon icon="info"
                   width="60"
                   height="60"
                   :original="true"
                   class="btn-round"
                   stroke="0"></svgicon>

          <a href="/about">About</a>
        </div>
      </li>

    </ul>
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
