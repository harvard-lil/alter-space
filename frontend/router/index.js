import Vue from 'vue';
import Router from 'vue-router';
import Sounds from '@/components/Sounds';
import Lights from '@/components/Lights';

Vue.use(Router);

export default new Router({
  routes: [
    {
    },
    {
      path: '/sounds',
      name: 'Sounds',
      component: Sounds
    },
    {
      path: '/lights',
      name: 'Lights',
      component: Lights
    }
  ]
});