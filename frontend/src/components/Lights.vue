<template>
  <div class="col-centered col-6">
    <h4> Choose lights</h4>
    <div class="description">

      <p>Enter a label like "Table Lamp" and a MAC address like "12:45:56:99:9a:bc"</p>
      <p>Labels must be unique.</p>

    </div>
    <div v-if="lightsFound.length > 0">
      <h6>All discoverable lights:</h6>
      <ul>
        <li v-for="light in lightsFound">
          <label><b>{{fixLabel(light[0])}}</b></label>
          &nbsp;&nbsp;&nbsp;{{light[1]}}
        </li>
      </ul>
    </div>


    <div class="col-12 alert-danger">{{error1}}</div>
    <div class="col-12 alert-danger">{{error2}}</div>
    <br/>

    <div>
      <p>Feel free to change the labels. They will update on submit.</p>
    </div>

    <table class="table col-12 light-list">
      <tr v-for="val in maxLights" class="list-inline-item" v-bind:key="val">
        <td>
          <label>Label #{{val}}: </label><input/>
        </td>
        <td>
          <label>MAC: </label><input/>
        </td>
        <td>
          <svgicon icon="lightbulb"
                   v-if="$route.params.name !== 'wyrd'"
                   width="30"
                   height="30"
                   :original="true"
                   class="btn-round btn-breathe"
                   stroke="0">
          </svgicon>
        </td>
      </tr>
    </table>
    <div class="col-12 alert-success" v-if="successMessage">{{successMessage}}<br/><br/></div>
    <br/>
    <button type="submit"
            class="btn-primary" @click="setLights()" :disabled="disabled">Update
    </button>
  </div>

</template>

<script>
  import axios from "axios";
  import './icons/lightbulb';

  const storeLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights/create";
  const getLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights";
  const discoverLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights/discover";
  const maxLights = process.env.VUE_APP_MAX_LIGHTS;

  export default {
    name: "Lights",
    data() {
      return {
        maxLights: Number(maxLights),
        lights: [],
        error1: "",
        error2: "",
        successMessage: "",
        disabled: false,
        lightsFound: [],
      }
    },
    methods: {
      discoverLights() {
        let self = this;
        axios.get(discoverLightsUrl)
            .then((res) => {
              self.lightsFound = res.data;
            })
      },
      getLights() {
        let self = this;
        let inputs = this.$el.querySelectorAll("input");
        let localStorageLights = [];
        axios.get(getLightsUrl)
            .then((res) => {
              let label = "";
              let lightNum = 0;
              for (let i = 0; i < res.data.length * 2; i++) {
                if (i % 2 === 0) {
                  lightNum = i / 2;
                  label = self.fixLabel(res.data[lightNum][0]);
                  console.log("getting label:", label);
                  inputs[i].value = label;
                } else {
                  inputs[i].value = res.data[lightNum][1];
                  localStorageLights.push([res.data[lightNum][0], res.data[lightNum][1]])
                }
              }
              localStorage.setItem("lights", JSON.stringify(localStorageLights));
            })

      },
      setLights() {
        let allLights = this.$el.querySelectorAll("input");
        let key = "";
        let val = "";
        let light = [];
        this.error1 = "";
        this.error2 = "";
        this.disabled = true;
        let count = 0;
        for (let i = 0; i < allLights.length; i++) {
          if (i % 2 === 0) {
            light = [];
            key = count.toString() + "_" + allLights[i].value;
            light.push(key)
            count += 1;
          } else {
            val = allLights[i].value;
            if (val.length && key.length) {
              light.push(val);
              this.lights.push(light);
            } else if (val.length && !(key.length)) {
              this.error1 = "All lights need a label";
              this.disabled = false;
              return
            }
          }
        }

        let bodyFormData = new FormData();
        bodyFormData.set('lights', JSON.stringify(this.lights));
        let self = this;

        if (self.lights.length > 0) {
          axios({
            method: "post",
            url: storeLightsUrl,
            data: bodyFormData
          }).then(() => {
            localStorage.clear();
            console.log("getting lights:", self.lights);
            localStorage.setItem("lights", JSON.stringify(self.lights));
            self.successMessage = "Success! " + self.lights.length + " light(s) created.";
            this.disabled = false;
          }).catch((res) => {
            this.error1 = res;
            this.disabled = false;
          });
        }
      },
      fixLabel(label) {
        let parts = label.split("_");
        parts.splice(0, 1);
        return parts.join("_");

      }
    },

    mounted() {
      this.getLights();
      this.discoverLights();
    }
  }
</script>