<template>
  <table align="center">
    <tr v-for="(level, l_idx) in activities" v-bind:key="l_idx">
      <td v-for="activity in activities[l_idx]" :key="activity">
        <router-link :id="activity"
                     :to="{ path: 'activity/' + activity}">
          <button class="btn btn-activity"
                  v-if="activity === 'wyrd'">
            w3!rd
          </button>
          <button class="btn btn-activity"
                  v-else>
            {{activity}}
          </button>

        </router-link>
      </td>
    </tr>

  </table>
</template>

<script>
  const activitiesUrl = process.env.VUE_APP_BACKEND_URL + "activities";

  export default {
    name: "Activities",
    props: ["translation"],
    data() {
      return {
        activities: [],
      }
    },
    methods: {
      getActivities() {
        fetch(activitiesUrl)
            .then((res) => {
              if (!res.ok) {
                throw res;
              }
              return res.json();
            })
            .then((res) => {
              let activities = res;
              let activtiesPerRow = 3;
              let loops = (activities.length / activtiesPerRow);
              let loop = 0;
              let activitiesForRendering = [];
              while (loop < loops) {
                activitiesForRendering.push(activities.slice(loop * 3, loop * 3 + 3));
                loop += 1;
              }
              this.activities = activitiesForRendering;
            })
      }
    },
    created() {
      this.getActivities();
    }
  }
</script>

