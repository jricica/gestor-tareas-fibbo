<template>
    <div class="signup">
        <div class="signup-card">
            <h1>Registrarse</h1>
            <form @submit.prevent="signup">
                <div class="input-group">
                    <input v-model="username" placeholder="Usuario" required />
                </div>
                <div class="input-group">
                    <input v-model="email" type="email" placeholder="Correo electrónico" required />
                </div>
                <div class="input-group">
                    <input v-model="password" type="password" placeholder="Contraseña" required />
                </div>
                <button type="submit" class="signup-btn">Crear cuenta</button>
            </form>
            <p class="login-link">
                ¿Ya tienes cuenta?
                <router-link to="/login">Inicia sesión</router-link>
            </p>
        </div>
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
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #e0e7ff 0%, #f9fafb 100%);
}

.signup-card {
    background: #fff;
    padding: 2.5rem 2rem;
    border-radius: 1.25rem;
    box-shadow: 0 6px 32px rgba(0,0,0,0.10);
    width: 100%;
    max-width: 420px;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

h1 {
    text-align: center;
    color: #3730a3;
    margin-bottom: 0.5rem;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 1px;
}

.input-group {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    margin-bottom: 1.5rem;
}

input {
    padding: 1rem 1.2rem;
    border: 1.5px solid #c7d2fe;
    border-radius: 0.7rem;
    font-size: 1.08rem;
    background: #f3f4f6;
    transition: border-color 0.2s, box-shadow 0.2s;
    outline: none;
    box-shadow: 0 1px 4px rgba(99,102,241,0.04);
}

input:focus {
    border-color: #6366f1;
    box-shadow: 0 2px 8px rgba(99,102,241,0.10);
    background: #fff;
}

.signup-btn {
    background: linear-gradient(90deg, #6366f1 60%, #818cf8 100%);
    color: #fff;
    border: none;
    padding: 0.9rem 1.2rem;
    border-radius: 0.7rem;
    font-size: 1.15rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    margin-top: 1rem;
    box-shadow: 0 2px 8px rgba(99,102,241,0.10);
}

.signup-btn:hover {
    background: linear-gradient(90deg, #4338ca 60%, #6366f1 100%);
    transform: translateY(-2px) scale(1.03);
}

.login-link {
    text-align: center;
    font-size: 1.05rem;
    margin-top: 2rem;
    letter-spacing: 0.2px;
}

.login-link a {
    color: #6366f1;
    text-decoration: underline;
    font-weight: 600;
    margin-left: 0.3rem;
    transition: color 0.2s;
}

.login-link a:hover {
    color: #4338ca;
}
</style>
