import Vue from 'vue';
import Router from 'vue-router';
import Sounds from '@/components/Sounds';
import Lights from '@/components/Lights';
import Activity from '@/components/Activity';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home'
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
    },
    {
      path: '/activity',
      name: 'Activity',
      component: Activity
    }
  ]
});