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
  </div>
</template>

<script>
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
