<template>
  <form method='post'>
    <table width="80%" align="center">
      <tbody>
      <tr>
        <th colspan="4">
          What sounds do you want to hear?
        </th>
      </tr>

       <th colspan="1" v-for="audio in audioFiles" :key="audio">
        <!--TODO: make a component out of this -->
        <audio loop controls>
          <source :id="audio" :src="`${audioBaseUrl}/${audio}`" type="audio/mpeg">
        </audio>
         <p>{{audio}}</p>
       </th>
        </tbody>
    </table>
  </form>

</template>

<script>
  import axios from 'axios';
  const audioBaseUrl = process.env.BASE_URL + "sounds";

  export default {
    name: "Sounds",
    data() {
      return {
        baseUrl: process.env.BASE_URL,
        audioBaseUrl: audioBaseUrl,
        audioFiles: []
      }
    },
    methods: {
      getFiles() {
        const path = 'http://localhost:5000/sounds';
        axios.get(path)
            .then((res) => {
              this.audioFiles = res.data
            })
      }
    },
    created() {
      this.getFiles()
    }
  }
</script>

<style scoped>

  form {
    margin-top: 20%;
  }

  .toggle {
    background-color: blue;
    color: white;
    padding: 10px;
    margin: 0 0 20px 0;
    width: 150px;
    cursor: pointer;
    font-weight: 300;
  }

  .toggle.on {
    background-color: navy;
  }
</style>
