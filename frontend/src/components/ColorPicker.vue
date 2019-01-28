<template>
  <div>
    <!-- preview element -->
    <ul class="list-inline">
      <li class="list-inline-item">
        <button class="btn-round"></button>
      </li>
      <li class="list-inline-item">
        <button class="btn-round"></button>
      </li>
      <li class="list-inline-item">
        <button class="btn-round"></button>
      </li>
    </ul>


  </div>

</template>

<script>
  export default {
    name: "ColorPicker",
    data() {
      return {
        hexVal: "#ffffff",
        src: require('../assets/img/colorwheel.jpg'),
        showColorPicker: false,
      }
    },
    methods: {
      // canvasImage() {
      //   let canvas = this.$refs.canvas;
      //   let ctx = canvas.getContext('2d');
      //   let img = this.$refs.secretImage;
      //   img.addEventListener("load", function () {
      //     ctx.drawImage(img, 0, 0, 300, 300);
      //     img.style.display = 'none';
      //   }, false);
      // },
      // getColor(e) {
      //   // Thank you https://www.script-tutorials.com/html5-color-picker-canvas/
      //   let offsetObj = this.$refs.canvas.getBoundingClientRect();
      //   let canvasOffset = {
      //     top: offsetObj.top + window.document.body.scrollTop,
      //     left: offsetObj.left + window.document.body.scrollLeft
      //   };
      //
      //   let canvasX = Math.floor(e.clientX - canvasOffset.left);
      //   let canvasY = Math.floor(e.clientY - canvasOffset.top);
      //
      //   // get current pixel
      //   let ctx = this.$refs.canvas.getContext('2d');
      //   let imageData = ctx.getImageData(canvasX, canvasY, 1, 1);
      //   let pixel = imageData.data;
      //
      //   // update lights' color
      //   let color = pixel[2] + 256 * pixel[1] + 65536 * pixel[0];
      //   this.hexVal = '#' + ('0000' + color.toString(16)).substr(-6);
      //   // TODO: post to light endpoint
      // }
    },
    mounted: function () {
      // this.canvasImage();
    }
  }
</script>

<style scoped>

</style>