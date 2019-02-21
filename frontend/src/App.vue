<template>
  <div id="app"
       :class="['app-activity-'+$route.params.name, {
       home: $route.name === 'Home'
       }]">

    <topnav :translation="translation"></topnav>


    <!-- Top level navigation -->
    <div class="container-fluid">
      <router-view :key="$route.fullPath"></router-view>

      <template v-if="$route.name === 'Home'">
        <div class="row">
          <div class="col-8 header col-centered text-center">
            <h5>
              Welcome to
            </h5>
            <h3 class="crazy-font">
              ALTeRsPaCe
            </h3>
            <h5 class="question-text">
              What would you like to do today?
            </h5>
          </div>
        </div>
        <Activities :translation="translation"></Activities>
      </template>
    </div>
  </div>
</template>


<script>

  import topnav from './components/TopNav';
  import Activities from './components/Activities';
  import "./components/icons/home";
  import "./components/icons/info";

  export default {
    name: 'app',
    components: {
      topnav,
      Activities,
    },
    data() {
      return {
        light: "",
        translation: {
          'relax': 'ReLaX',
          'read': 'READ',
          'focus': 'FOcUs',
          'create': 'cREATe',
          'meditate': 'mEdITAtE',
          'wyrd': 'W3!Rd',
        }
      }
    },
    mounted() {
      this.light = localStorage.getItem("light");
      if (!(this.light)) {
        this.$router.replace('/light');
      }
    }
  }
</script>