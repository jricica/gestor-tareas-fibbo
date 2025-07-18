﻿# 🗂️ Gestor de Tareas Fibbo

Aplicación web de gestión de tareas con autenticación, tareas propias y compartidas, desarrollada con Vue.js, Django REST Framework y PostgreSQL.

---

## 🧰 Tecnologías usadas

- 🔧 **Frontend**: Vue 3 + Vite
- ⚙️ **Backend**: Django + Django REST Framework + Simple JWT
- 🛢️ **Base de datos**: PostgreSQL (local)
- 📦 **Dependencias**: Axios, Vue Router, JWT Decode

---

## 🚀 Funcionalidades

- Registro e inicio de sesión de usuarios
- CRUD completo de tareas
- Tareas propias y tareas compartidas con otros usuarios
- Interfaz responsiva y sencilla
- Panel principal con listado de tareas
- Filtro visual de tareas por usuario

---

## 📦 Instalación local

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/gestor-tareas-fibbo.git
cd gestor-tareas-fibbo
gestor-tareas-fibbo/
├── backend/
│   ├── tasks/
│   ├── users/
│   ├── config/
│   └── manage.py  
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── views/
│   │   ├── api/
│   │   ├── assets/
│   │   ├── router
│   │   ├── components/
│       └── App.vue, main.js, etc.
├── img/
```
### 2. Backend (Django)
```bash
cd backend
python -m venv env
source env/bin/activate        # En Windows: env\Scripts\activate
pip install -r requirements.txt
```
#### Crear base de datos en PostgreSQL:
Configura tu ``` settings.py ``` con tus credenciales PostgreSQL:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fibbo_db',
        'USER': 'postgres',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
#### Aplicar migraciones y ejecutar el servidor:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
### 3. Frontend (Vue)
```bash
cd ../frontend
npm install
npm run dev
```
## 🔐 Endpoints principales (API)
| Método | Endpoint          | Descripción                          |
| ------ | ----------------- | ------------------------------------ |
| POST   | `/api/signup/`    | Registro de usuario                  |
| POST   | `/api/token/`     | Login (obtener JWT)                  |
| GET    | `/api/tasks/`     | Listar tareas del usuario            |
| POST   | `/api/tasks/`     | Crear tarea                          |
| PUT    | `/api/tasks/:id/` | Actualizar tarea                     |
| DELETE | `/api/tasks/:id/` | Eliminar tarea                       |
| GET    | `/api/users/`     | Obtener lista de usuarios (frontend) |

## Imágenes
En la carpeta ```img``` se encuentran capturas de pantalla del programa

## 🧑‍💻 Autor
### Jan Ricica
