// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import SvgIcon from 'vue-svgicon';

import App from './App'
import router from '../router'
import './assets/css/styles.scss';

Vue.config.productionTip = false;

/* eslint-disable no-new */

Vue.use(SvgIcon, {
  tagName: 'svgicon',
  defaultWidth: '1em',
  defaultHeight: '1em'
});


new Vue({
  el: '#app',
  components: {App},
  template: '<App/>',
  router: router
});

