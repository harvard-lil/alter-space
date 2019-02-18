<template>
  <ul class="nav"
      :class="'activity-'+$route.params.name">
    <li class="nav-item col-2">
      <div class="button-label-container">
        <router-link to="/"
        class="nav-button-group">
          <svgicon icon="home"
                   width="45"
                   height="45"
                   class="icon btn-round"
                   stroke="0"></svgicon>
          <br/>
          Home</router-link>
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
        <a href="/about" class="nav-button-group">
          <svgicon icon="info"
                   width="45"
                   height="45"
                   class="icon btn-round"
                   stroke="0"></svgicon>

          <br/>
          About</a>
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