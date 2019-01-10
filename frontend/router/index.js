import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Sounds from '@/components/Sounds';
import Lights from '@/components/Lights';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
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