<template>
  <div id="app"
       :class="'app-activity-'+$route.params.name">

    <topnav :translation="translation"></topnav>
    <template v-if="$route.name === 'preset'">
      <preset :translation="translation"></preset>
    </template>


    <template v-else>
      <!-- Top level navigation -->
      <div class="container-fluid">
        <router-view :key="$route.fullPath"></router-view>

        <template v-if="$route.name === 'Home'">
          <div class="row">
            <div class="col-8 col-centered">
              <h4 class="text-center">
                Welcome to
              </h4>
              <h1 class="text-center">
                ALTeRsPaCe
              </h1>
              <h5 class="text-center">
                What would you like to do today?
              </h5>
            </div>
          </div>
          <Activities></Activities>
        </template>
      </div>
    </template>
  </div>
</template>


<script>

  import topnav from './components/TopNav';
  import Activities from './components/Activities';
  import Preset from './components/Preset';

  import "./components/icons/home";
  import "./components/icons/info";

  export default {
    name: 'app',
    components: {
      topnav,
      Preset,
      Activities
    },
    data() {
      return {
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
  }
</script>