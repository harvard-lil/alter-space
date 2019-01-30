<template>
  <div class="row light-levers">
    <div class="col-12">
      <h3>Lights</h3>
    </div>
    <div class="col-12">
      <table class="table cell-table">
        <tr>
          <td>
            <color-picker></color-picker>
            <label>colors</label>
          </td>
          <td>
            <!--TODO: breathe effect-->
            <button class="btn-round"></button>
            <label>breathe</label>
          </td>
          <td>
            <brightness-slider></brightness-slider>
            <label>brightness</label>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
  import ColorPicker from './ColorPicker';
  import BrightnessSlider from './BrightnessSlider';

  export default {
    components: {ColorPicker, BrightnessSlider},
    name: "LightLevers"
  }
</script>
