<template>
  <ul class="nav"
      :class="'activity-'+$route.params.name">
    <!--<div class="btn-group">-->
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
    <li class="nav-item col-8">
      <h1 class="page-header"
          v-if="$route.name === 'activity' && $route.params.name">
        {{translation[$route.params.name]}}
      </h1>
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
</template>

<script>
  export default {
    name: "topnav",
    props: ['translation'],
  }
</script>

<style scoped>

</style>