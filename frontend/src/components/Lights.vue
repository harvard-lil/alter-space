<template>
  <div class="col-centered col-6">
    <h4> Choose lights</h4>
    <div class="description">
      Make sure you're connected to the correct WiFi.
      Lights might not show up immediately.
    </div>
    <div v-if="lightsFound.length > 0">
      <h6>All discoverable lights:</h6>
      <ul style="padding-left: 0;">
        <li class="light-finding-list-item" v-bind:key="light[1]" v-for="light in lightsFound">
          <span>
            <b>{{light[0]}}</b>
            {{light[1]}}
          </span>
          <button v-if="light[0] in lights"
                  :class="[{progress: currentMACAddress === light[1], }, 'btn-remove-light btn-light btn-default']"
                  @click="removeLight(light[0], light[1])">Remove Light
          </button>
          <button v-else
                  :class="[{progress: currentMACAddress === light[1]}, 'btn-add-light btn-light btn-default']"
                  @click="addLight(light[0], light[1])">Add light
          </button>
          <br/>
          <button @click="flickerLight(light[0], light[1])"
                  :class="{flickering: currentMACAddress === light[1] && isFlickering, 'btn-default btn-flicker':true}">
            Flicker
          </button>
        </li>
      </ul>
    </div>


    <div class="col-12 alert-danger">{{error1}}</div>
    <div class="col-12 alert-danger">{{error2}}</div>
    <br/>
  </div>

</template>

<script>
  import axios from 'axios';

  import './icons/lightbulb';

  const getLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights";
  const storeLightsUrl = getLightsUrl + "/create";
  const discoverLightsUrl = getLightsUrl + "/discover";
  const flickerLightUrl = getLightsUrl + "/flicker";
  const maxLights = process.env.VUE_APP_MAX_LIGHTS;

  export default {
    name: "Lights",
    data() {
      return {
        maxLights: Number(maxLights),
        lights: {},
        error1: "",
        error2: "",
        successMessage: "",
        currentLightLabel: "",
        currentMACAddress: "",
        disabled: false,
        lightsFound: [],
        isFlickering: false
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
        /* gets lights that have been previously selected for use */
        let localStorageLights = [];
        let self = this;
        axios.get(getLightsUrl)
            .then((res) => {
              let label = "";
              let lightNum = 0;
              for (let i = 0; i < res.data.length * 2; i++) {
                if (i % 2 === 0) {
                  lightNum = i / 2;
                  label = res.data[lightNum][0];
                  self.lights[label] = ""
                } else {
                  localStorageLights.push([res.data[lightNum][0], res.data[lightNum][1]])
                  self.lights[label] = res.data[lightNum][1];
                }
              }
              localStorage.setItem("lights", JSON.stringify(localStorageLights));
            })

      },
      removeLight(label, mac_addr) {
        delete this.lights[label];
        this.currentLightLabel = label;
        this.currentMACAddress = mac_addr;
        this.updateLights();

      },
      addLight(label, mac_addr) {
        this.lights[label] = mac_addr;
        this.currentLightLabel = label;
        this.currentMACAddress = mac_addr;
        this.updateLights();
      },
      updateLights() {
        let data = {
          lights: JSON.stringify(this.lights)
        };
        let self = this;
        axios({
          url: storeLightsUrl,
          method: "post",
          data: data
        }).then(() => {
          localStorage.clear();
          let localStorageLights = [];
          for (let light in self.lights) {
            localStorageLights.push([light, self.lights[light]]);
          }
          localStorage.setItem("lights", JSON.stringify(localStorageLights));
          self.successMessage = "Success! " + localStorageLights.length + " light(s) created.";
          self.disabled = false;
          self.currentLightLabel = "";
          self.currentMACAddress = "";
        });
      },

      flickerLight(label, mac_addr) {
        let data = {
          label: label,
          mac_addr: mac_addr
        };
        this.currentLightLabel = label;
        this.currentMACAddress = mac_addr;
        this.isFlickering = true;
        let self = this;
        axios({
          url: flickerLightUrl,
          method: "post",
          data: data
        }).then(() => {
          self.currentLightLabel = "";
          self.currentMACAddress = "";
          self.isFlickering = false;
        })
      }
    },

    mounted() {
      this.discoverLights();
      this.getLights();
    }
  }
</script>