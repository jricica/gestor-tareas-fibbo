<template>
  <div class="tasks">
    <h2>Mis tareas</h2>

    <form @submit.prevent="createTask">
      <input v-model="title" type="text" placeholder="Título" required />
      <input v-model="description" type="text" placeholder="Descripción" required />
      <select v-model="priority">
        <option value="low">Baja</option>
        <option value="medium">Media</option>
        <option value="high">Alta</option>
      </select>
      <input v-model="dueDate" type="date" required />
      <select v-model="status">
        <option value="pending">Pendiente</option>
        <option value="in_progress">En progreso</option>
        <option value="completed">Completada</option>
      </select>
      <button type="submit">
        {{ editingTaskId ? 'Actualizar' : 'Agregar' }} tarea
      </button>
    </form>

    <ul>
      <li v-for="task in tasks" :key="task.id">
        <strong>{{ task.title }}</strong> - {{ task.status }}
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

export default {
  setup() {
    const router = useRouter();
    const tasks = ref([]);

    const title = ref('');
    const description = ref('');
    const priority = ref('low');
    const dueDate = ref('');
    const status = ref('pending');
    const editingTaskId = ref(null);

    const fetchTasks = async () => {
      const token = localStorage.getItem('access');
      if (!token) {
        console.warn('No hay token, redirigiendo a login');
        router.push('/login');
        return;
      }

      try {
        console.log('Usando token:', token);
        const res = await api.get('/tasks/');
        tasks.value = res.data;
      } catch (err) {
        console.error('Error al obtener tareas:', err.response?.data || err.message);
        if (err.response?.status === 401) {
          logout();
        } else if (err.response?.status === 500) {
          alert('Error interno del servidor al cargar tareas.');
        }
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
        };

        if (editingTaskId.value) {
          await api.put(`/tasks/${editingTaskId.value}/`, payload);
        } else {
          await api.post('/tasks/', payload);
        }

        await fetchTasks();
        clearForm();
      } catch (err) {
        console.error('Error al guardar tarea:', err.response?.data || err.message);
        if (err.response?.status === 401) logout();
      }
    };

    const deleteTask = async (id) => {
      try {
        await api.delete(`/tasks/${id}/`);
        await fetchTasks();
      } catch (err) {
        console.error('Error al eliminar tarea:', err.response?.data || err.message);
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
    };

    const clearForm = () => {
      editingTaskId.value = null;
      title.value = '';
      description.value = '';
      dueDate.value = '';
      status.value = 'pending';
      priority.value = 'low';
    };

    const logout = () => {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      router.push('/login');
    };

    onMounted(() => {
      fetchTasks();
    });

    return {
      tasks,
      title,
      description,
      priority,
      dueDate,
      status,
      createTask,
      deleteTask,
      editTask,
      logout,
      editingTaskId,
    };
  },
};
</script>

<style scoped>
.tasks {
  max-width: 600px;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 2rem;
}
</style>
