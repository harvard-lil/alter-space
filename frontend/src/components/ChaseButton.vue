<template>
  <div class="td col-2">
    <svgicon icon="chase"
             width="60"
             height="60"
             :original="true"
             class="btn-round btn-chase"
             @click="toggleChase()"
             :class="{active: chase}"
             stroke="0"></svgicon>

    <label v-if="chase">stop</label>
    <label v-else>chase</label>
  </div>

</template>

<script>
  import axios from 'axios';
  import "./icons/chase";

  const chaseUrl = process.env.VUE_APP_BACKEND_URL + "lights/effects" + "/chase";

  export default {
    name: "chase-button",
    data() {
      return {
        chase: false,
        taskID: ""
      }
    },
    methods: {
      toggleChase() {
        let self = this;
        self.chase = !(self.chase);
        let bodyFormData = new FormData();
        bodyFormData.set('id', self.$parent.light);
        bodyFormData.set('effect', self.chase);
        if (self.taskID) {
          bodyFormData.set('task_id', self.taskID);
        }

        axios({
          method: "post",
          url: chaseUrl,
          data: bodyFormData
        }).then((res) => {
          self.taskID = res.data.task_id;
          self.$parent.effectPlaying = self.chase;
          if (!(self.chase)) {
            EventBus.$emit('reset-brightness', self.breathe);
          }

        })
      },
    }

  }
</script>
