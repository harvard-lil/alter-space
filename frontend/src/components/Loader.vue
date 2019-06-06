<template>
  <div class="btn-round btn-loader"
        :class="typeOfLoader">
    <div id="floatingCirclesG">
      <div class="f_circleG" id="frotateG_01"></div>
      <div class="f_circleG" id="frotateG_02"></div>
      <div class="f_circleG" id="frotateG_03"></div>
      <div class="f_circleG" id="frotateG_04"></div>
      <div class="f_circleG" id="frotateG_05"></div>
      <div class="f_circleG" id="frotateG_06"></div>
      <div class="f_circleG" id="frotateG_07"></div>
      <div class="f_circleG" id="frotateG_08"></div>
    </div>
  </div>

</template>

<script>
  export default {
    name: "loader",
    props: ["typeOfLoader"]
  }
</script>

<style scoped>
  /* loader */
  /* thanks https://icons8.com/cssload/ ! */
  .btn-round {
    background-color: #260066;
    position: relative;
    width: 60px;
    height: 60px;
    box-shadow: none;
  }
  .btn-round.playbutton {
    background-color: #ff6666;
  }

  #floatingCirclesG {
    position: absolute;
    width: 125px;
    height: 125px;
    margin-top: -32px;
    border-radius: 50%;
    padding: 20px;
    margin-left: -33px;
    transform: scale(0.3);
    -o-transform: scale(0.3);
    -ms-transform: scale(0.3);
    -webkit-transform: scale(0.3);
    -moz-transform: scale(0.3);
  }

  .f_circleG {
    position: absolute;
    background-color: white;
    height: 22px;
    width: 22px;
    border-radius: 12px;
    -o-border-radius: 12px;
    -ms-border-radius: 12px;
    -webkit-border-radius: 12px;
    -moz-border-radius: 12px;
    animation-name: f_fadeG;
    -o-animation-name: f_fadeG;
    -ms-animation-name: f_fadeG;
    -webkit-animation-name: f_fadeG;
    -moz-animation-name: f_fadeG;
    animation-duration: 1.2s;
    -o-animation-duration: 1.2s;
    -ms-animation-duration: 1.2s;
    -webkit-animation-duration: 1.2s;
    -moz-animation-duration: 1.2s;
    animation-iteration-count: infinite;
    -o-animation-iteration-count: infinite;
    -ms-animation-iteration-count: infinite;
    -webkit-animation-iteration-count: infinite;
    -moz-animation-iteration-count: infinite;
    animation-direction: normal;
    -o-animation-direction: normal;
    -ms-animation-direction: normal;
    -webkit-animation-direction: normal;
    -moz-animation-direction: normal;
  }

  #frotateG_01 {
    left: 0;
    top: 51px;
    animation-delay: 0.45s;
    -o-animation-delay: 0.45s;
    -ms-animation-delay: 0.45s;
    -webkit-animation-delay: 0.45s;
    -moz-animation-delay: 0.45s;
  }

  #frotateG_02 {
    left: 15px;
    top: 15px;
    animation-delay: 0.6s;
    -o-animation-delay: 0.6s;
    -ms-animation-delay: 0.6s;
    -webkit-animation-delay: 0.6s;
    -moz-animation-delay: 0.6s;
  }

  #frotateG_03 {
    left: 51px;
    top: 0;
    animation-delay: 0.75s;
    -o-animation-delay: 0.75s;
    -ms-animation-delay: 0.75s;
    -webkit-animation-delay: 0.75s;
    -moz-animation-delay: 0.75s;
  }

  #frotateG_04 {
    right: 15px;
    top: 15px;
    animation-delay: 0.9s;
    -o-animation-delay: 0.9s;
    -ms-animation-delay: 0.9s;
    -webkit-animation-delay: 0.9s;
    -moz-animation-delay: 0.9s;
  }

  #frotateG_05 {
    right: 0;
    top: 51px;
    animation-delay: 1.05s;
    -o-animation-delay: 1.05s;
    -ms-animation-delay: 1.05s;
    -webkit-animation-delay: 1.05s;
    -moz-animation-delay: 1.05s;
  }

  #frotateG_06 {
    right: 15px;
    bottom: 15px;
    animation-delay: 1.2s;
    -o-animation-delay: 1.2s;
    -ms-animation-delay: 1.2s;
    -webkit-animation-delay: 1.2s;
    -moz-animation-delay: 1.2s;
  }

  #frotateG_07 {
    left: 51px;
    bottom: 0;
    animation-delay: 1.35s;
    -o-animation-delay: 1.35s;
    -ms-animation-delay: 1.35s;
    -webkit-animation-delay: 1.35s;
    -moz-animation-delay: 1.35s;
  }

  #frotateG_08 {
    left: 15px;
    bottom: 15px;
    animation-delay: 1.5s;
    -o-animation-delay: 1.5s;
    -ms-animation-delay: 1.5s;
    -webkit-animation-delay: 1.5s;
    -moz-animation-delay: 1.5s;
  }

  @keyframes f_fadeG {
    0% {
      background-color: #260066;
    }

    100% {
      background-color: white;
    }
  }

  @-o-keyframes f_fadeG {
    0% {
      background-color: #260066;
    }

    100% {
      background-color: white;
    }
  }

  @-ms-keyframes f_fadeG {
    0% {
      background-color: #260066;
    }

    100% {
      background-color: white;
    }
  }

  @-webkit-keyframes f_fadeG {
    0% {
      background-color: #260066;
    }

    100% {
      background-color: white;
    }
  }

  @-moz-keyframes f_fadeG {
    0% {
      background-color: #260066;
    }

    100% {
      background-color: white;
    }
  }


</style>