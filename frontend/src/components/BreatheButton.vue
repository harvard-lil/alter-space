<template>
  <div class="td col-2">
    <!--TODO: breathe effect-->
    <svgicon icon="breathe"
             width="60"
             height="60"
             :original="true"
             class="btn-round btn-breathe"
             @click="toggleBreathe()"
             :class="{active: breathe}"
             stroke="0"></svgicon>

    <label v-if="breathe">stop</label>
    <label v-else>breathe</label>
  </div>

</template>

<script>
  import axios from 'axios';
  import EventBus from '../event-bus'

  const breatheUrl = process.env.VUE_APP_BACKEND_URL + "lights" + "/breathe"
  export default {
    name: "breathe-button",
    data() {
      return {
        breathe: false,
        taskID: ""
      }
    },
    methods: {
      toggleBreathe() {
        let self = this;
        self.breathe = !(self.breathe);
        let bodyFormData = new FormData();
        bodyFormData.set('id', self.$parent.light);
        bodyFormData.set('breathe', self.breathe);
        if (self.taskID) {
          bodyFormData.set('task_id', self.taskID);
        }

        axios({
          method: "post",
          url: breatheUrl,
          data: bodyFormData
        }).then((res) => {
          self.taskID = res.data.task_id;
          if (!(self.breathe)) {
            EventBus.$emit('reset-brightness', self.breathe);
          }
        })
      },
    }

  }
</script>
