# Tienda # 🧠 Proyecto Django - Aplicación Web

Este repositorio contiene una aplicación desarrollada con Django, lista para ejecutarse en entorno local. Incluye pasos para levantar el entorno virtual, instalar dependencias, crear superusuario y correr el servidor de desarrollo.

---

## 🛠️ Requisitos previos

- Python 3.10+
- pip
- Git (opcional pero recomendado)
- Virtualenv (opcional pero recomendado)

---

## ⚙️ Configuración del entorno

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu_usuario/tu_repo.git
cd tu_repo

# 2. Crear y activar entorno virtual
python -m venv env
# En Windows
env\Scripts\activate
# En Linux/MacOS
source env/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones iniciales
python manage.py migrate

```

## 👤 Crear superusuario

```bash
python manage.py createsuperuser
# Sigue las instrucciones (usuario, correo, contraseña)
```
Abre tu navegador en: http://127.0.0.1:8000

## 🚀 Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

## 🔐 Acceso al panel de administración

Ir a http://127.0.0.1:8000/admin

Iniciar sesión con las credenciales del superusuario creado

