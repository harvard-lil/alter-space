<template>
  <table width="80%" align="center">
    <tbody>
    <tr>
      <th colspan="4">
        What's your color?
        <input v-model="colorString"
                class="color"
                @input="getColor">
        <p>hex is: {{ color }} color string is {{ colorString }}</p>
      </th>
    </tr>

    <th colspan="4">
      <button type="submit">Submit</button>
    </th>

    </tbody>
  </table>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "Lights",
    data() {
      return {
        color: "#fffff",
        colorString: "white",
        colorModel: {}
      }
    },
    methods: {
      getColor() {
        const path = 'http://localhost:5000/lights';

        if (this.colorString.length === 0) {
          return
        }
        axios.get(path, {
          params: {
            color: this.color,
            color_string: this.colorString
          }
        })
            .then((res) => {
              this.color = res.data.color;
              this.colorString = res.data.color_string;

              let body = document.getElementsByTagName('body')[0]
              body.style.backgroundColor = this.color;
            })
      },

    }
  }
</script>
