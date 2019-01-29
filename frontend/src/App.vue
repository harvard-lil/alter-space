<template>
  <div id="app" :class="'activity-'+$route.query.name">
    <!-- Top level navigation -->

    <nav class="nav"
         :class="'activity-'+$route.query.name">
      <div class="row">
        <div class="col-1">
          <div class="btn-group">
            <a class="btn-link btn-home"
               href="/"></a>
            <a href="/">Home</a>
          </div>
        </div>
        <div class="col-10">
          <h1 class="page-header"
              v-if="$route.query.name && $route.query.name !== 'wyrd'"
              :class="'activity-'+$route.query.name">
            {{ $route.query.name }}
          </h1>
          <h1 class="page-header"
              v-else-if="$route.query.name === 'wyrd'"
              :class="'activity-'+$route.query.name">
            w3!rd
          </h1>

        </div>
        <div class="col-1">
          <div class="btn-group">
            <a class="btn-link btn-info" href="/about"></a>
            <a href="/about">About</a>
          </div>
        </div>
      </div>
    </nav>

    <router-view :key="$route.fullPath"></router-view>

    <div class="container"
         v-if="$route.name === 'Home'">
      <div class="row">
        <div class="col-8 col-centered">
          <h4 class="text-center">Welcome to</h4>
          <h1 class="text-center">
            Alterspace
          </h1>
        </div>
      </div>
      <div class="row">
        <Activities></Activities>
      </div>
    </div>
  </div>
</template>


<script>
  import Activities from './components/Activities'
  import EventBus from './event-bus';

  export default {
    name: 'app',
    components: {Activities},
    data() {
      return {
        showModal: false,
      }
    },
    mounted() {
      EventBus.$on('modal', function (modalStatus) {
        this.showModal = modalStatus;
      });
    }
  }
</script>