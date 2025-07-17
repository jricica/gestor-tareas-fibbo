<template>
  <div class="tasks-view">
    <h1>Gestión de Tareas</h1>

    <!-- Formulario -->
    <form @submit.prevent="createTask">
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

      <select v-model="sharedWith" multiple>
        <option v-for="user in users" :key="user.id" :value="user.id">
          {{ user.username }}
        </option>
      </select>

      <button type="submit">
        {{ editingTaskId ? 'Actualizar' : 'Crear' }} Tarea
      </button>
      <button type="button" @click="clearForm">Limpiar</button>
    </form>

    <hr />

    <!-- Lista de Tareas -->
    <ul>
      <li v-for="task in tasks" :key="task.id">
        <strong>{{ task.title }}</strong> ({{ task.status }}) - Prioridad: {{ task.priority }}
        <br />
        {{ task.description }}
        <br />
        <button @click="editTask(task)">Editar</button>
        <button @click="deleteTask(task.id)">Eliminar</button>
      </li>
    </ul>

    <button @click="logout">Cerrar sesión</button>
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
      sharedWith.value = task.shared_with || [];
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
    };
  },
};
</script>

<style scoped>
.tasks-view {
  max-width: 600px;
  margin: auto;
  padding: 1rem;
}
</style>
