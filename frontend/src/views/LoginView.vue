<template>
    <div class="login">
        <div class="login-card">
            <h1>Iniciar Sesión</h1>
            <form @submit.prevent="login">
                <div class="input-group">
                    <input
                        v-model="username"
                        type="text"
                        placeholder="Usuario"
                        required
                    />
                    <input
                        v-model="password"
                        type="password"
                        placeholder="Contraseña"
                        required
                    />
                </div>
                <button class="login-btn" :disabled="loading" type="submit">
                    <span v-if="loading" class="spinner"></span>
                    <span v-else>Entrar</span>
                </button>
            </form>
            <p v-if="error" class="error-message">{{ error }}</p>
            <p class="signup-link">
                ¿No tienes cuenta?
                <router-link to="/signup">Regístrate aquí</router-link>
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
const loading = ref(false);
const error = ref('');
const router = useRouter();

const login = async () => {
    loading.value = true;
    error.value = '';

    try {
        const response = await api.post('/token/', {
            username: username.value,
            password: password.value,
        });

        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);
        router.push('/tasks');
    } catch (err) {
        console.error('Login error:', err.response?.data || err);
        error.value = 'Credenciales inválidas. Intenta de nuevo.';
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.login {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #e0e7ff 0%, #f9fafb 100%);
}

.login-card {
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

.login-btn {
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
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-btn[disabled] {
    background: #a5b4fc;
    cursor: not-allowed;
}

.login-btn:hover:not([disabled]) {
    background: linear-gradient(90deg, #4338ca 60%, #6366f1 100%);
    transform: translateY(-2px) scale(1.03);
}

.spinner {
    width: 18px;
    height: 18px;
    border: 3px solid white;
    border-top: 3px solid transparent;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.signup-link {
    text-align: center;
    font-size: 1.05rem;
    margin-top: 2rem;
    letter-spacing: 0.2px;
}

.signup-link a {
    color: #6366f1;
    text-decoration: underline;
    font-weight: 600;
    margin-left: 0.3rem;
    transition: color 0.2s;
}

.signup-link a:hover {
    color: #4338ca;
}

.error-message {
    color: #e74c3c;
    text-align: center;
    margin-top: 0.5rem;
}
</style>
