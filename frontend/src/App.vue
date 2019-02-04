<template>
  <div id="app"
       :class="'app-activity-'+$route.params.name">

    <template v-if="$route.name === 'preset'">
      <preset :translation="translation"></preset>
    </template>


    <template v-else>
      <!-- Top level navigation -->

      <ul class="nav" :class="'activity-'+$route.params.name">
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
              v-if="$route.params.name"
              :class="'activity-'+$route.params.name">
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

  import Activities from './components/Activities';
  import Preset from './components/Preset';

  import "./components/icons/home";
  import "./components/icons/info";

  export default {
    name: 'app',
    components: {
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