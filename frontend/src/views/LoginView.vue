<!-- src/views/LoginView.vue -->
<template>
  <div class="login">
    <h1>Iniciar Sesión</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Usuario" />
      <input v-model="password" type="password" placeholder="Contraseña" />
      <button type="submit">Entrar</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/axios';

const username = ref('');
const password = ref('');
const router = useRouter();

const login = async () => {
  try {
    const response = await api.post('/token/', {
      username: username.value,
      password: password.value,
    });

    console.log('Login response:', response.data); 

    localStorage.setItem('access', response.data.access);
    localStorage.setItem('refresh', response.data.refresh);
    router.push('/tasks');
  } catch (error) {
    console.error('Login error:', error.response?.data || error);
    alert('Credenciales inválidas');
  }
};
</script>
