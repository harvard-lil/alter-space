<template>
  <div class="col-centered col-6">
    <h4> Choose lights</h4>
    <div class="description">
      Enter a label like "Table Lamp" and a MAC address like "12:45:56:99:9a:bc"
    </div>
    <div class="col-12 alert-danger">{{error1}}</div>
    <div class="col-12 alert-danger">{{error2}}</div>
    <br/>

    <table class="col-12 light-list">
      <tr v-for="val in maxLights" class="list-inline-item" v-bind:key="val">
        <td>
          <label>Label #{{val}}: </label><input/>
        </td>
        <td>
          <label>Mac address: </label><input/>
        </td>
      </tr>
    </table>
    <input type="submit" @click="setLights()" value="Submit">
    <div class="col-12 alert-success">{{successMessage}}</div>
  </div>
</template>

<script>
  import axios from "axios";

  const storeLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights/create";
  const getLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights";
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
      }
    },
    methods: {

      getLights() {
        let self = this;
        let inputs = this.$el.querySelectorAll("td");
        let localStorageLights = [];
        axios.get(getLightsUrl)
            .then((res) => {
              let lightNum = 0;
              for (let i = 0; i < res.data.length * 2; i++) {
                if (i % 2 === 0) {
                  lightNum = i / 2;
                  inputs[i].getElementsByTagName('input')[0].value = res.data[lightNum][0];
                } else {
                  inputs[i].getElementsByTagName('input')[0].value = res.data[lightNum][1];
                  localStorageLights.push([res.data[lightNum][0], res.data[lightNum][1]])
                }
              }
              localStorage.setItem("lights", JSON.stringify(localStorageLights));
            })

      },
      setLights() {
        let allLights = this.$el.querySelectorAll("td");
        let key = "";
        let val = "";
        let light = [];
        this.error1 = "";
        this.error2 = "";
        for (let i = 0; i < allLights.length; i++) {
          if (i % 2 === 0) {
            light = [];
            key = allLights[i].getElementsByTagName('input')[0].value;
            light.push(key)
          } else {
            val = allLights[i].getElementsByTagName('input')[0].value;
            if (val.length && key.length) {
              light.push(val);
              this.lights.push(light);
            } else if (val.length && !(key.length)) {
              this.error1 = "All lights need a label";
              return
            }
            if (!(val.length) && key.length) {
              this.error2 = "Please enter the MAC address for each light."
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
            localStorage.setItem("lights", JSON.stringify(self.lights));
            self.successMessage = "Success! " + self.lights.length + " light(s) created.";
          });
        }
      },
    },

    mounted() {
      this.getLights();
    }
  }
</script>