<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 to-indigo-200 flex items-center justify-center px-4">
    <div class="bg-white p-8 md:p-10 rounded-2xl shadow-xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-center text-indigo-600 mb-6">Iniciar Sesión</h1>

      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Usuario</label>
          <input
            v-model="username"
            placeholder="Tu nombre de usuario"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input
            v-model="password"
            type="password"
            placeholder="Tu contraseña"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-lg shadow-md transition"
        >
          Entrar
        </button>
      </form>

      <p class="text-center text-sm mt-6 text-gray-600">
        ¿No tienes cuenta?
        <router-link to="/signup" class="text-indigo-600 hover:underline font-medium">Regístrate aquí</router-link>
      </p>
    </div>
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

    localStorage.setItem('access', response.data.access);
    localStorage.setItem('refresh', response.data.refresh);
    router.push('/tasks');
  } catch (error) {
    console.error('Login error:', error.response?.data || error);
    alert('Credenciales inválidas');
  }
};
</script>
