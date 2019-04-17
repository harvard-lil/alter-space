<template>
  <div id="app"
       :class="['app-activity-'+$route.params.name, $route.name]">

    <topnav :translation="translation"></topnav>


    <!-- Top level navigation -->
    <div class="container-fluid">
      <router-view :key="$route.fullPath"></router-view>

      <template v-if="$route.name === 'home'">
        <div class="row">
          <div class="col-8 header col-centered text-center">
            <h4 class="welcome-text">
              Welcome to
            </h4>
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

  import axios from "axios";
  import topnav from './components/TopNav';
  import Activities from './components/Activities';
  import "./components/icons/home";
  import "./components/icons/info";
  const getLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights";

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
      this.lights = localStorage.getItem("lights");
      if (!(this.lights)) {
        axios.get(getLightsUrl)
            .then((res) => {
              let light = [];
              let localStorageLights = [];
              for (let i = 0; i < res.data.length; i++) {
                light = [res.data[i][0], res.data[i][1]];
                localStorageLights.push(light);
              }
              localStorage.setItem("lights", JSON.stringify(localStorageLights));
            })
      }
    }
  }
</script>