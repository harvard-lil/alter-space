<template>
  <ul>
    <li v-for="activity in activities" :key="activity">
      <router-link :id="activity" :to="{ path: 'Activity', query: { name: activity }}">
        <button class="activity-button">{{activity}}</button>
      </router-link>
    </li>
  </ul>
</template>

<script>
  import axios from 'axios';

  const activitiesUrl = process.env.VUE_APP_BACKEND_URL + "activities";

  export default {
    name: "Activities",
    data() {
      return {
        activities: []
      }
    },
    methods: {
      getActivities() {
        axios.get(activitiesUrl)
            .then((res) => {
              this.activities = res.data;
              window.activities = this.activities;
            })
            .catch(function () {
              window.errors = arguments
            })
      }
    },
    created() {
      this.getActivities()
    }
  }
</script>

<style lang="scss">

  ul {
    list-style: none;
  }
</style>