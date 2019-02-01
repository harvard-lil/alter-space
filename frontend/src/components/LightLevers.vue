<template>
  <div class="row light-levers">
    <div class="col-12">
      <h3>Lights</h3>
    </div>
    <div class="col-12">
      <table class="table cell-table table-top">
        <tr>
          <td width="30%">
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

          </td>
          <td width="20%">
            <!--TODO: breathe effect-->
            <button class="btn-breathe"></button>
            <label>breathe</label>
          </td>
          <td width="50%">
            <brightness-slider></brightness-slider>
            <label>brightness</label>
          </td>
        </tr>
      </table>
    </div>
    <div class="col-12">
      <table class="table cell-table table-bottom"
             v-show="showingList">
        <tr>
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
        </tr>
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
  </div>
</template>

<script>
  import axios from 'axios';

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
