<template>
  <div class="container-preset row"
       :class="'activity-'+$route.params.name">
    <div class="preset-content text-center">
      <h1>
        {{translation[$route.params.name]}}
      </h1>
      <router-link
              :to="{ path: '/activity/' + $route.params.name}">

        <button class="btn btn-customize"
                :class="$route.params.name">
          Customize!
        </button>
      </router-link>
    </div>
    <!-- playing activity in the background -->
    <activity v-show="false"></activity>
  </div>

</template>

<script>
  import Activity from './Activity'

  export default {
    name: "preset",
    props: ["translation"],
    components: {Activity},
    data() {
      return {}
    }
  }

</script>
