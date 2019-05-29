<template>
  <div class="row light-levers">
    <div class="title-shape">
      <svgicon icon="triangle-light"
               width="100%"
               height="100%"
               title="Light Levers"
               class="triangle"
               :class="$route.params.name"
               stroke="0">
      </svgicon>

    </div>
    <div class="table cell-table table-top-single"
         :class="[$route.params.name, {
            options: showingList
         }]">
      <div class="tr">
        <div class="td col-4">
          <!-- Light list start -->
          <div class="btn-group-color"
               role="group"
               aria-label="color button group">
            <ul class="light-group list-inline light-list">
              <li class="list-inline-item" v-bind:key="label" v-for="label in lightLabels">
                <!--if lightbulb or single zone light-->
                <svgicon icon="lightbulb"
                         class="btn-round btn-color"
                         v-bind:key="label"
                         width="40"
                         height="40"
                         :disabled="disableColors"
                         stroke="0"
                         @click="showList(label)"
                         :class="{active: colorPresets[getIdxFromLightLabel(label)] === colorPresets[getIdxFromLightLabel(currentLightLabel)] && showingList && currentLightLabel === label, lightbulb: true}"
                         :style="{'fill': colorPresets[getIdxFromLightLabel(label)]}">

                </svgicon>


                <button class="btn-round-tiny btn-power"
                        :class="{active: lightStates[label] }"
                        @click="togglePower(label)"></button>
              </li>
            </ul>
            <!--if light is multizone-->
            <ul class="light-group list-inline light-list">
              <li class="list-inline-item" v-bind:key="label" v-for="label in multizoneLightLabels">
                <svgicon icon="lightgradient"
                         class="btn-round btn-color"
                         v-bind:key="label"
                         width="40"
                         height="40"
                         :disabled="disableColors"
                         stroke="0"
                         @click="showList(label)"
                         :class="{active: colorPresets[getIdxFromLightLabel(label)] === colorPresets[getIdxFromLightLabel(currentLightLabel)] && showingList && currentLightLabel === label,
                         lightgradient: true}">
                </svgicon>
                <button class="btn-round-tiny btn-power"
                        :class="{active: lightStates[label] }"
                        @click="togglePower(label)"></button>
              </li>
            </ul>
            <!--<ul class="gradient-example list-inline">
              <li class="gradient-pixel list-inline-item"
                  v-for="(pixel, idx) in colorGradient"
                  v-bind:key="idx"
                  :style="{'backgroundColor': pixel}"></li>
            </ul>-->

            <label class="text-center">colors </label>
          </div>
          <!-- Light list end -->
        </div>
        <div class="td col-8">
          <brightness-slider :disable="disableBrightness">
          </brightness-slider>
          <label>brightness</label>
        </div>
      </div>
    </div>
    <table class="table cell-table table-bottom"
           :class="$route.params.name"
           v-show="showingList">
      <div class="btn-group-color-options col-centered"
           :class="[$route.params.name, {disabled: disableColors}]"
           role="group"
           aria-label="color button group">
        <template v-if="isMultizoneLight(currentLightLabel)">
          <div class="helper-text">This light has multiple color zones. Choose up to {{ maxMultizoneValues }}.</div>
          <button type="button"
                  v-for="(hexVal, idx) in colors"
                  v-bind:key="idx"
                  @click="chooseMultizoneColor(hexVal)"
                  :class="{active: multizoneValues[currentLightLabel].colors.indexOf(hexVal) > -1, 'btn-round-small': true, 'btn-color-option': true}"
                  :style="{'backgroundColor': hexVal}">
          </button>
        </template>
        <template v-else>

          <svgicon icon="arrow-up"
                   class="arrow-up colors"
                   :class="['color-'+getIdxFromLightLabel(currentLightLabel), $route.params.name]">
          </svgicon>

          <button type="button"
                  class="btn-round-small btn-color-option"
                  v-for="(hexVal, idx) in colors"
                  v-bind:key="idx"
                  :id="hexVal"
                  @click="chooseNewColor(hexVal)"
                  :style="{'backgroundColor': hexVal}">
          </button>
        </template>
      </div>
    </table>
  </div>
</template>

<script>
  import axios from 'axios';

  import './icons/breathe';
  import './icons/triangle-light';
  import './icons/arrow-up';
  import './icons/lightbulb';
  import './icons/lightgradient';
  import EventBus from '../event-bus';

  import BrightnessSlider from './BrightnessSlider';

  const colorsUrl = process.env.VUE_APP_BACKEND_URL + "lights" + "/colors";
  const getLightsUrl = process.env.VUE_APP_BACKEND_URL + "lights";
  const setLightUrl = process.env.VUE_APP_BACKEND_URL + "lights" + "/set";

  // steps between color 1 and color 2
  const steps = 8;

  export default {
    name: "LightLevers",
    components: {
      // EffectButton,
      BrightnessSlider
    },
    props: ["lightPresets", "collapseLightOptions", "effectOn"],
    data() {
      return {
        showColorPicker: false,
        colorPresets: [],
        multicolorPresets: [],
        colors: [],
        showingList: false,
        currentLightLabel: "",
        light: "",
        lights: [],
        lightLabels: [],
        multizoneLightLabels: [],
        lightStates: {},
        colorGradient: [],
        multizoneValues: {}, // this object stores multiple color values for lights that are multizone
        maxMultizoneValues: 3,
        brightness: 100,
        effectPlaying: false,
        disableBrightness: false,
        disableColors: false,
        disableEffect: false,
        effectInPreset: "",
        firstCall: true,
      }
    },
    watch: {
      lightPresets() {
        if (this.colorPresets.length === 0) {
          this.colorPresets = this.lightPresets.colors;
          this.multicolorPresets = this.lightPresets.multicolors;
          for (let i = 0; i < this.lightLabels.length; i++) {
            this.currentLightLabel = this.lightLabels[i];
            this.setLight();
          }
          for (let m = 0; m < this.multizoneLightLabels.length; m++) {
            this.currentLightLabel = this.multizoneLightLabels[m];
            this.multizoneValues[this.currentLightLabel].colors = this.lightPresets.multicolors[m];
            this.createGradient();
            this.setMultizoneLights();
          }
        }
      },
      collapseLightOptions() {
        if (this.collapseLightOptions) {
          this.showingList = false;
          this.$parent.showingLightOptions = false;
        }
      },
      effectPlaying() {
        let toDisable = this.effectPlaying;
        this.disableBrightness = toDisable;
        this.disableColors = toDisable;
        if (toDisable) {
          this.showingList = false;
        }
      }
    },
    methods: {
      showList(label) {
        if (!(this.showingList)) {
          this.showingList = true;
        } else if (this.currentLightLabel === label || this.currentLightLabel === "") {
          this.showingList = !this.showingList;
        }
        this.currentLightLabel = label;
        this.$parent.showingLightOptions = this.showingList;
      },

      createGradient() {
        let colors = this.multizoneValues[this.currentLightLabel].colors;
        let colorSteps = [];
        this.multizoneValues[this.currentLightLabel].gradient = [];
        for (let i = 0; i < colors.length; i++) {
          this.multizoneValues[this.currentLightLabel].gradient.push(colors[i]);
        }
        for (let d = 0; d < colors.length - 1; d++) {
          colorSteps = this.interpolateColors(colors[d], colors[d + 1], steps);
          colorSteps.shift();
          this.multizoneValues[this.currentLightLabel].gradient.push(colorSteps);
        }
        this.multizoneValues[this.currentLightLabel].gradient = this.multizoneValues[this.currentLightLabel].gradient.flat();
      },
      setLight() {
        let bodyFormData = new FormData();
        if (!(this.currentLightLabel)) {
          console.log("no light defined, returning");
          return
        }

        bodyFormData.set('label', this.currentLightLabel);
        let idx = this.getIdxFromLightLabel(this.currentLightLabel);
        bodyFormData.set('color', this.colorPresets[idx]);
        bodyFormData.set('bright', this.brightness.toString());
        bodyFormData.set('firstcall', this.firstCall);

        axios({
          method: "post",
          url: setLightUrl,
          data: bodyFormData,
        }).then(() => {
          self.disableEffect = false;
          self.disableColors = false;
          self.disableBrightness = false;
          self.firstCall = false;
        })
      },
      setMultizoneLights() {
        let bodyFormData = new FormData();
        let d = {color_data: this.multizoneValues[this.currentLightLabel].gradient};
        bodyFormData.set('id', this.light);
        bodyFormData.set('bright', this.brightness.toString());
        bodyFormData.set('label', this.currentLightLabel);
        bodyFormData.set('firstcall', this.firstCall);
        bodyFormData.set('multicolors', JSON.stringify(d));
        //disabling all buttons until results are backs
        this.disableEffect = true;
        this.disableColors = true;
        this.disableBrightness = true;
        let self = this;

        axios({
          method: "post",
          url: setLightUrl,
          data: bodyFormData,
        }).then(() => {
          self.disableEffect = false;
          self.disableColors = false;
          self.disableBrightness = false;
          self.firstCall = false;
        })
      },
      chooseNewColor(hexVal) {
        let idx = this.getIdxFromLightLabel(this.currentLightLabel);
        // using splice instead of something more simple because of vuejs's array change detection:
        // https://vuejs.org/v2/guide/list.html#Array-Change-Detection
        this.colorPresets.splice(idx, 1, hexVal);
        this.setLight()
      },

      chooseMultizoneColor(hexVal) {
        // if the current light is not yet stored in our multizone values object, create it
        if (Object.keys(this.multizoneValues).indexOf(this.currentLightLabel) < 0) {
          this.multizoneValues[this.currentLightLabel] = {
            colors: [],
            gradient: []
          };
        }

        // if we've reached our max colors (as defined by this.maxMultizoneValues), push the first one (oldest choice) out
        if (this.multizoneValues[this.currentLightLabel].colors.length >= this.maxMultizoneValues) {
          this.multizoneValues[this.currentLightLabel].colors.shift();
          this.multizoneValues[this.currentLightLabel].colors.push(hexVal);
        }
        this.createGradient();
        this.setMultizoneLights();
      },
      
      getLSLights() {
        this.lights = JSON.parse(localStorage.getItem('lights'));
        // create an array of just labels for ease of use
        // TODO: Figure out if this is dangerous. Are lights *always* going to be ordered this way?
        for (let i = 0; i < this.lights.length; i++) {
          // this.lightLabels.push(i.toString() + "_" + this.lights[i][0]);
          let label = this.lights[i][0];

          // if multizone, set up the object
          if (this.isMultizoneLight(label)) {
            this.multizoneValues[label] = {
              colors: [],
              gradient: []
            };
            this.multizoneLightLabels.push(label);
          } else {
            this.lightLabels.push(label);
          }
        }
      },
      setLightStates() {
        for (let i = 0; i < this.lightLabels.length; i++) {
          this.lightStates[this.lightLabels[i]] = true;
          this.togglePower(this.lightLabels[i], true)
        }
        for (let i = 0; i < this.multizoneLightLabels.length; i++) {
          this.lightStates[this.multizoneLightLabels[i]] = true;
          this.togglePower(this.lightLabels[i], true);
        }

      },
      // From https://codepen.io/njmcode/pen/axoyD?editors=0010
      rgb2hex(rgb) {
        return "#" + ((1 << 24) + (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]).toString(16).slice(1);
      },

      hex2rgb(hex) {
        let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? [
          parseInt(result[1], 16),
          parseInt(result[2], 16),
          parseInt(result[3], 16)
        ] : null;
      },
      // From https://graphicdesign.stackexchange.com/a/83867
      interpolateColor(color1, color2, factor) {
        if (arguments.length < 3) {
          factor = 0.5;
        }
        let result = color1.slice();
        for (let i = 0; i < 3; i++) {
          result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
        }
        let newcolor = this.rgb2hex(result);
        console.log("%c color " + newcolor, "color: " + newcolor);
        return newcolor;
      },

      interpolateColors(color1, color2, steps) {
        color1 = this.hex2rgb(color1);
        color2 = this.hex2rgb(color2);
        let stepFactor = 1 / (steps - 1),
            interpolatedColorArray = [];

        for (let i = 0; i < steps; i++) {
          let interpolated = this.interpolateColor(color1, color2, stepFactor * i);
          interpolatedColorArray.push(interpolated);
        }
        return interpolatedColorArray;
      },

      getIdxFromLightLabel(lightLabel) {
        return this.lightLabels.indexOf(lightLabel);
      },

      isMultizoneLight(label) {
        return label.indexOf('_multizone_') > -1;
      },

      togglePower(label, powerState) {
        let currentState = this.lightStates[label];
        let toState = powerState ? powerState : !(currentState);
        this.lightStates[label] = toState;
        this.currentLightLabel = label;

        let powerUrl = getLightsUrl + "/power";
        let bodyFormData = new FormData();
        bodyFormData.set('label', this.currentLightLabel);
        bodyFormData.set('to_status', toState);
        //disabling all buttons until results are backs
        this.disableEffect = true;
        this.disableColors = true;
        this.disableBrightness = true;
        let self = this;

        axios({
          method: "post",
          url: powerUrl,
          data: bodyFormData,
        }).then((res) => {
          self.disableEffect = false;
          self.disableColors = false;
          self.disableBrightness = false;
        })
      },
    },
    beforeMount() {
      let self = this;
      axios.get(getLightsUrl).then((res) => {
        self.lights = res.data;
      });
      /* get available colors */
      axios.get(colorsUrl).then((res) => {
        self.colors = res.data;
      });
    },
    mounted() {
      let self = this;
      EventBus.$on('update-brightness', (brightness) => {
        self.brightness = brightness;
      });

    },
    created() {
      this.getLSLights();
      this.setLightStates();
    },
  }

</script>