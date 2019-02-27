<template>
  <div class="td col-2">
    <svgicon icon="breathe"
             width="60"
             height="60"
             :original="true"
             class="btn-round btn-breathe"
             @click="toggleBreathe()"
             :class="{active: breathe, disabled: disable}"
             stroke="0"></svgicon>

    <label v-if="breathe">stop</label>
    <label v-else>breathe</label>
  </div>

</template>

<script>
  import axios from 'axios';
  import EventBus from '../event-bus'
  import "./icons/breathe";
  const breatheUrl = process.env.VUE_APP_BACKEND_URL + "lights/effects" + "/breathe";

  export default {
    name: "breathe-button",
    props: ["disable"],
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
        bodyFormData.set('light_id', self.$parent.light);
        bodyFormData.set('effect', self.breathe);
        bodyFormData.set('breathe_type', self.$route.params.name);
        if (self.taskID) {
          bodyFormData.set('task_id', self.taskID);
        }

        axios({
          method: "post",
          url: breatheUrl,
          data: bodyFormData
        }).then((res) => {
          self.taskID = res.data.task_id;
          self.$parent.$parent.taskID = self.taskID;
          self.$parent.effectPlaying = self.breathe;
          self.$parent.$parent.effect = "breathe";
          if (!(self.breathe)) {
            EventBus.$emit('reset-brightness', self.breathe);
          }
        })
      },
    }

  }
</script>
