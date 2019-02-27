<template>
  <ul class="nav"
      :class="['activity-'+$route.params.name, {about: $route.name === 'about'}]">
    <li class="nav-item col-2">
      <div class="button-label-container">
        <router-link to="/"
        class="nav-button-group">
          <svgicon icon="home"
                   width="45"
                   height="45"
                   class="icon btn-round btn-nav"
                   stroke="0"></svgicon>
          <br/>
          Home</router-link>
      </div>
    </li>
    <li class="nav-item col-8">
      <h1 class="page-header"
          v-if="$route.name === 'activity' && $route.params.name && customizing">
        {{translation[$route.params.name]}}
      </h1>
      <h1 class="page-header" v-if="$route.name === 'about'">ABOuT</h1>
    </li>
    <li class="nav-item col-2" v-if="$route.name !== 'about'">
      <div class="button-label-container">
        <router-link to="/about" class="nav-button-group">
          <svgicon icon="info"
                   width="45"
                   height="45"
                   class="icon btn-round btn-nav"
                   stroke="0"></svgicon>

          <br/>
          About</router-link>
      </div>
    </li>
  </ul>
</template>

<script>
  import EventBus from '../event-bus'
  export default {
    name: "topnav",
    props: ['translation'],
    data() {
      return {
        customizing: false
      }
    },
    mounted() {
      let self = this;
      // showing name of activity in nav or not
      EventBus.$on('customizing', (customizing) => {
        self.customizing = customizing;
      })
    }
  }
</script>