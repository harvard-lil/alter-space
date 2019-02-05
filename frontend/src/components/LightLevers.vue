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
    <div class="table cell-table table-top-single" :class="$route.params.name">
      <div class="tr">
        <div class="td col-4">
          <div class="btn-group-color"
               role="group"
               aria-label="color button group">

            <button type="button"
                    class="btn-round btn-color"
                    v-for="(color, idx) in colorPresets"
                    v-bind:key="idx"
                    @click="showList(idx)"
                    :class="{active: color === colorPresets[currentColorIdx]}"
                    :style="{'backgroundColor': color}">
            </button>
            <label class="text-center">colors</label>
          </div>

        </div>
        <div class="td col-2">
          <!--TODO: breathe effect-->
          <svgicon icon="breathe"
                   width="60"
                   height="60"
                   :original="true"
                   class="btn-round"
                   stroke="0"></svgicon>

          <label>breathe</label>
        </div>
        <div class="td col-6">
          <brightness-slider></brightness-slider>
          <label>brightness</label>
        </div>
      </div>
    </div>
    <table class="table cell-table table-bottom"
           v-show="showingList">
      <div class="tr">
        <th class="row">
          <div class="col-6">
            Choose a new color
          </div>
          <div class="col-6 text-right">
            <a @click="showingList=false">
              Back to main view
              <span class="btn-x"></span>
            </a>
          </div>
        </th>
      </div>
      <div class="btn-group-color-options col-centered"
           role="group"
           aria-label="color button group">

        <button type="button"
                class="btn-round-small btn-color"
                v-for="hexVal in colors"
                v-bind:key="hexVal"
                @click="chooseNewColor(hexVal)"
                :style="{'backgroundColor': hexVal}">
        </button>
      </div>
    </table>
  </div>
</template>

<script>
  import axios from 'axios';
  import './icons/breathe';
  import './icons/triangle-light';

  import BrightnessSlider from './BrightnessSlider';

  const colorsUrl = process.env.VUE_APP_BACKEND_URL + "lights" + "/colors";

  export default {
    components: {BrightnessSlider},
    name: "LightLevers",
    data() {
      return {
        showColorPicker: false,
        colorPresets: ["#ff6666", "#fbd6e8", "#fbb03b"],
        colors: [],
        showingList: false,
        currentColorIdx: "",
      }
    },
    methods: {
      showList(idx) {
        if (!(this.showingList)) {
          this.showingList = true;
        } else if (this.currentColorIdx === idx || this.currentColorIdx === "") {
          this.showingList = !this.showingList;
        }
        this.currentColorIdx = idx;
      },
      chooseNewColor(hexVal) {
        this.colorPresets.splice([this.currentColorIdx], 1, hexVal);
        // TODO: change lights here
      }
    },
    beforeMount() {
      axios.get(colorsUrl).then((res) => {
        this.colors = res.data;
      })
    }

  }
</script>
