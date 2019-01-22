<template>
  <div id="app">
    <!-- Top level navigation -->
    <nav class="nav">
      <a href="/">Home</a>
    </nav>

    <router-view :key="$route.fullPath">
    </router-view>
    <div class="container">
      <div class="row">
        <div class="col-8 col-centered">
          <h4 class="text-center">Welcome to</h4>
          <h1 class="text-center">
            Alterspace
          </h1>
        </div>
      </div>
      <div class="row">
        <!--<div class="col-12">-->
          <Activities></Activities>
        <!--</div>-->
      </div>
    </div>
  </div>
</template>


<script>
  import Activities from './components/Activities'

  export default {
    name: 'app',
    components: {Activities}
  }
</script>