<template>
    <div class="tasks-bg">
        <div class="tasks-card">
            <h1>Gestión de Tareas</h1>

            <!-- Formulario -->
            <form @submit.prevent="createTask">
                <div class="input-group">
                    <input v-model="title" placeholder="Título" required />
                    <textarea v-model="description" placeholder="Descripción"></textarea>
                    <select v-model="priority">
                        <option value="low">Baja</option>
                        <option value="medium">Media</option>
                        <option value="high">Alta</option>
                    </select>
                    <input type="date" v-model="dueDate" />
                    <select v-model="status">
                        <option value="pending">Pendiente</option>
                        <option value="in_progress">En progreso</option>
                        <option value="completed">Completada</option>
                    </select>
                    <div class="checkbox-group">
                        <label>Compartir con:</label>
                        <div class="checkbox-list">
                            <label v-for="user in users" :key="user.id" class="checkbox-item">
                                <input
                                    type="checkbox"
                                    :value="user.id"
                                    v-model="sharedWith"
                                />
                                {{ user.username }}
                            </label>
                        </div>
                    </div>
                </div>
                <button type="submit" class="tasks-btn">
                    {{ editingTaskId ? 'Actualizar' : 'Crear' }} Tarea
                </button>
                <button type="button" class="tasks-btn secondary" @click="clearForm">Limpiar</button>
            </form>

            <hr />

            <!-- Lista de Tareas -->
            <ul class="tasks-list">
                <li v-for="task in tasks" :key="task.id" class="task-item">
                    <div class="task-header">
                        <strong>{{ task.title }}</strong>
                        <span class="chip" :class="'priority-' + task.priority">
                            {{ task.priority.charAt(0).toUpperCase() + task.priority.slice(1) }}
                        </span>
                        <span class="chip" :class="'status-' + task.status">
                            {{ statusLabel(task.status) }}
                        </span>
                        <span v-if="task.due_date" class="chip due-date">
                            Vence: {{ task.due_date }}
                        </span>
                    </div>
                    <div>{{ task.description }}</div>
                    <div v-if="task.shared_with && task.shared_with.length" class="shared-users">
                        <span class="chip shared-chip" v-for="uid in task.shared_with" :key="uid">
                            {{ usernameById(uid) }}
                        </span>
                    </div>
                    <div class="task-actions">
                        <button @click="editTask(task)" class="tasks-btn small">Editar</button>
                        <button @click="deleteTask(task.id)" class="tasks-btn small secondary">Eliminar</button>
                    </div>
                </li>
            </ul>

            <button @click="logout" class="tasks-btn logout">Cerrar sesión</button>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/axios';
import { jwtDecode } from 'jwt-decode';

export default {
    setup() {
        const router = useRouter();
        const tasks = ref([]);
        const users = ref([]);
        const currentUserId = ref(null);

        const title = ref('');
        const description = ref('');
        const priority = ref('low');
        const dueDate = ref('');
        const status = ref('pending');
        const sharedWith = ref([]);
        const editingTaskId = ref(null);

        const fetchTasks = async () => {
            const token = localStorage.getItem('access');
            if (!token) {
                router.push('/login');
                return;
            }
            try {
                const decoded = jwtDecode(token);
                currentUserId.value = decoded.user_id;

                const res = await api.get('/tasks/');
                tasks.value = res.data;
            } catch (err) {
                if (err.response?.status === 401) logout();
            }
        };

        const fetchUsers = async () => {
            try {
                const res = await api.get('/users/');
                users.value = res.data.filter(user => user.id !== currentUserId.value);
            } catch (err) {
                console.error('Error al cargar usuarios:', err);
            }
        };

        const createTask = async () => {
            try {
                const payload = {
                    title: title.value,
                    description: description.value,
                    priority: priority.value,
                    due_date: dueDate.value,
                    status: status.value,
                    shared_with: sharedWith.value,
                };

                if (editingTaskId.value) {
                    await api.put(`/tasks/${editingTaskId.value}/`, payload);
                } else {
                    await api.post('/tasks/', payload);
                }

                await fetchTasks();
                clearForm();
            } catch (err) {
                if (err.response?.status === 401) logout();
            }
        };

        const deleteTask = async (id) => {
            try {
                await api.delete(`/tasks/${id}/`);
                await fetchTasks();
            } catch (err) {
                if (err.response?.status === 401) logout();
            }
        };

        const editTask = (task) => {
            editingTaskId.value = task.id;
            title.value = task.title;
            description.value = task.description;
            priority.value = task.priority;
            dueDate.value = task.due_date;
            status.value = task.status;
            sharedWith.value = task.shared_with ? [...task.shared_with] : [];
        };

        const clearForm = () => {
            editingTaskId.value = null;
            title.value = '';
            description.value = '';
            dueDate.value = '';
            status.value = 'pending';
            priority.value = 'low';
            sharedWith.value = [];
        };

        const logout = () => {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            router.push('/login');
        };

        // Helpers
        const usernameById = (id) => {
            const user = users.value.find(u => u.id === id);
            return user ? user.username : 'Usuario';
        };

        const statusLabel = (status) => {
            switch (status) {
                case 'pending': return 'Pendiente';
                case 'in_progress': return 'En progreso';
                case 'completed': return 'Completada';
                default: return status;
            }
        };

        onMounted(async () => {
            await fetchTasks();
            await fetchUsers();
        });

        return {
            tasks,
            users,
            title,
            description,
            priority,
            dueDate,
            status,
            sharedWith,
            createTask,
            deleteTask,
            editTask,
            logout,
            editingTaskId,
            clearForm,
            usernameById,
            statusLabel,
        };
    },
};
</script>

<style scoped>
.tasks-bg {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #e0e7ff 0%, #f9fafb 100%);
}

.tasks-card {
    background: #fff;
    padding: 2.5rem 2rem;
    border-radius: 1.25rem;
    box-shadow: 0 6px 32px rgba(0,0,0,0.10);
    width: 100%;
    max-width: 480px;
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

input,
textarea,
select {
    padding: 1rem 1.2rem;
    border: 1.5px solid #c7d2fe;
    border-radius: 0.7rem;
    font-size: 1.08rem;
    background: #f3f4f6;
    transition: border-color 0.2s, box-shadow 0.2s;
    outline: none;
    box-shadow: 0 1px 4px rgba(99,102,241,0.04);
    resize: none;
}

input:focus,
textarea:focus,
select:focus {
    border-color: #6366f1;
    box-shadow: 0 2px 8px rgba(99,102,241,0.10);
    background: #fff;
}

.tasks-btn {
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

.tasks-btn:hover {
    background: linear-gradient(90deg, #4338ca 60%, #6366f1 100%);
    transform: translateY(-2px) scale(1.03);
}

.tasks-btn.secondary {
    background: #f3f4f6;
    color: #6366f1;
    border: 1.5px solid #c7d2fe;
    margin-left: 0.7rem;
    box-shadow: none;
}

.tasks-btn.secondary:hover {
    background: #e0e7ff;
    color: #4338ca;
    border-color: #6366f1;
}

.tasks-btn.small {
    font-size: 0.98rem;
    padding: 0.5rem 1rem;
    margin-top: 0;
    margin-left: 0.5rem;
}

.tasks-btn.logout {
    background: linear-gradient(90deg, #f87171 60%, #fbbf24 100%);
    color: #fff;
    margin-top: 2rem;
    font-size: 1.08rem;
    font-weight: 700;
}

.tasks-btn.logout:hover {
    background: linear-gradient(90deg, #ef4444 60%, #f59e42 100%);
}

.checkbox-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.checkbox-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
}

.checkbox-item {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    background: #f3f4f6;
    padding: 0.3rem 0.7rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    border: 1px solid #e0e7ff;
}

.tasks-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.task-item {
    background: #f9fafb;
    border-radius: 1rem;
    box-shadow: 0 1px 8px rgba(99,102,241,0.06);
    padding: 1.2rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.task-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.3rem;
}

.chip {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 1rem;
    font-size: 0.95rem;
    font-weight: 600;
    margin-right: 0.2rem;
    background: #e0e7ff;
    color: #3730a3;
}

.chip.priority-low { background: #d1fae5; color: #065f46; }
.chip.priority-medium { background: #fef3c7; color: #92400e; }
.chip.priority-high { background: #fee2e2; color: #b91c1c; }

.chip.status-pending { background: #f3f4f6; color: #6b7280; }
.chip.status-in_progress { background: #dbeafe; color: #2563eb; }
.chip.status-completed { background: #bbf7d0; color: #166534; }

.chip.due-date { background: #f3f4f6; color: #7c3aed; }

.shared-users {
    margin: 0.5rem 0 0.2rem 0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}

.shared-chip {
    background: #ede9fe;
    color: #7c3aed;
    font-size: 0.92rem;
    padding: 0.15rem 0.6rem;
}

hr {
    border: none;
    border-top: 1.5px solid #e0e7ff;
    margin: 2rem 0 1.2rem 0;
}
</style>
