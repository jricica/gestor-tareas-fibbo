import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import TasksView from '../views/TasksView.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: TasksView,
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access');
  
  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else if (to.path === '/login' && token) {
    next('/tasks');
  } else {
    next();
  }
});

export default router;
