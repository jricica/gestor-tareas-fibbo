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
      <button type="submit">Agregar tarea</button>
    </form>

    <ul>
      <li v-for="task in tasks" :key="task.id">
        <strong>{{ task.title }}</strong> - {{ task.status }}
      </li>
    </ul>

    <button @click="logout">Cerrar sesión</button>
  </div>
</template>

<script>
import api from '../api/axios';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const tasks = ref([]);

    const title = ref('');
    const description = ref('');
    const priority = ref('low');
    const dueDate = ref('');
    const status = ref('pending');

    const fetchTasks = async () => {
      try {
        const res = await api.get('/tasks/');
        tasks.value = res.data;
      } catch (err) {
        router.push('/login');
      }
    };

    const createTask = async () => {
      try {
        await api.post('/tasks/', {
          title: title.value,
          description: description.value,
          priority: priority.value,
          due_date: dueDate.value,
          status: status.value,
        });
        await fetchTasks(); // recargar tareas
        // limpiar formulario
        title.value = '';
        description.value = '';
        dueDate.value = '';
        status.value = 'pending';
        priority.value = 'low';
      } catch (err) {
        console.error('Error al crear tarea', err);
      }
    };

    const logout = () => {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      router.push('/login');
    };

    onMounted(fetchTasks);

    return {
      tasks,
      title,
      description,
      priority,
      dueDate,
      status,
      createTask,
      logout,
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
