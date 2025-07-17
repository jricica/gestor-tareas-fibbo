<template>
  <div class="signup">
    <h1>Registrarse</h1>
    <form @submit.prevent="signup">
      <input v-model="username" placeholder="Usuario" required />
      <input v-model="email" type="email" placeholder="Correo electrónico" required />
      <input v-model="password" type="password" placeholder="Contraseña" required />
      <button type="submit">Crear cuenta</button>
    </form>
    <p>
      ¿Ya tienes cuenta?
      <router-link to="/login">Inicia sesión</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/axios';

const username = ref('');
const email = ref('');
const password = ref('');
const router = useRouter();

const signup = async () => {
  try {
    await api.post('/signup/', {
      username: username.value,
      email: email.value,
      password: password.value,
    });

    // Después de registrarse, pedir token
    const res = await api.post('/token/', {
      username: username.value,
      password: password.value,
    });

    localStorage.setItem('access', res.data.access);
    localStorage.setItem('refresh', res.data.refresh);
    router.push('/tasks');
  } catch (err) {
    console.error('Error en registro', err);
    alert('Registro fallido. Verifica los datos.');
  }
};
</script>

<style scoped>
.signup {
  max-width: 400px;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
