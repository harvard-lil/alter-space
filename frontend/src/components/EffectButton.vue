<template>
  <div class="td col-2">

    <svgicon icon="breathe"
             v-if="$route.params.name !== 'wyrd'"
             width="60"
             height="60"
             :original="true"
             class="btn-round btn-breathe"
             @click="toggleEffect()"
             :class="{active: effectStatus, disabled: disable}"
             stroke="0"></svgicon>

    <svgicon icon="chase"
             v-else
             width="60"
             height="60"
             :original="true"
             class="btn-round btn-chase"
             @click="toggleEffect()"
             :class="{active: effectStatus, disabled: disable}"
             stroke="0"></svgicon>

    <label v-if="effectStatus">stop</label>
    <label v-else-if="$route.params.name === 'relax'">slow breath</label>
    <label v-else>{{effectType}}</label>
  </div>

</template>

<script>
  import axios from 'axios';

  import EventBus from '../event-bus'
  import "./icons/breathe";
  import "./icons/chase";

  const effectUrl = process.env.VUE_APP_BACKEND_URL + "lights/effects";

  export default {
    name: "effect-button",
    props: ["disable", "effectInPreset"],
    data() {
      return {
        taskID: "",
        effectStatus: false,
        effectTimeout: null,
        effectType: "breathe"
      }
    },
    methods: {
      toggleEffect() {
        let self = this;
        self.effectStatus = !(self.effectStatus);
        let data = {
          light_id: self.$parent.light,
          effect: self.effectStatus
        };
        if (self.effectType === 'breathe') {
          data.breathe_type = self.$route.params.name;
        }
        if (self.taskID) {
          data.task_id = self.taskID;
        }

        let url = self.$route.params.name === 'wyrd' ? effectUrl + "/chase" : effectUrl + "/breathe";

        axios({
          method: "post",
          url: url,
          data: data
        }).then((res) => {
          self.taskID = res.data.task_id;
          self.$parent.$parent.taskID = self.taskID;
          self.$parent.effectPlaying = self.effectStatus;
          self.$parent.$parent.effect = self.effectType;
          if (!(self.effectStatus)) {
            EventBus.$emit('reset-brightness', self.effectStatus);
          }
        })
      },
    },
    mounted() {
      if (this.$route.params.name === 'wyrd') {
        this.effectType = 'chase';
      }
    },
    watch: {
      effectInPreset() {
        let self = this;
        this.effectTimeout = setTimeout(() => {
          self.toggleEffect();
        }, 3000);
      }
    },
    beforeDestroy() {
      clearTimeout(this.effectTimeout);
    }
  }
</script>
