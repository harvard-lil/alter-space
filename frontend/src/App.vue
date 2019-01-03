<template>
  <div id="app">
    <nav>
      <ul>
        <li>
          <router-link to="/">Home</router-link>
        </li>
        <li>
          <router-link to="/lights">Lights</router-link>
        </li>
        <li>
          <router-link to="/sounds">Sounds</router-link>
        </li>
      </ul>
    </nav>
    <router-view></router-view>
  </div>
</template>


<script>
  export default {
    name: 'app',
    components: {}
  }
</script>
