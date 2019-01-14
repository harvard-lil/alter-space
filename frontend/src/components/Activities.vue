<template>
  <div class="row">
    <div class="col-12">
      <ul>
        <li v-for="activity in activities" :key="activity">
          <router-link :id="activity"
                       :to="{ path: 'Activity', query: { name: activity }}">
            <button class="btn btn-primary btn-activity">{{activity}}</button>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
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

