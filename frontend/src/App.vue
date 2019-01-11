<template>
  <div id="app">
    <!-- Top level navigation -->
    <nav class="nav">
      <a href="/">Home</a>
    </nav>

    <router-view></router-view>
    <div class="container">
      <div class="row">
        <div class="col-4">
          <h2>Choose an activity</h2>
          <Activities></Activities>
        </div>
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