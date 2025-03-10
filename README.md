# turia_tests
# 📌 Microservicio Flask con SQLite

Este proyecto es un **microservicio en Python usando Flask y SQLite** que permite gestionar empleados con operaciones CRUD.

## 🚀 Características
- API RESTful con Flask
- Persistencia de datos en SQLite
- Pruebas automatizadas con `pytest`
- Documentación con Swagger usando `flasgger`

## 📂 Estructura del Proyecto
```
/turia_tests/
│── app/                         # Carpeta de la aplicación
│   ├── __init__.py               # Inicialización del módulo app
│   ├── app.py                    # Código principal de Flask
│── tests/                        # Carpeta de pruebas
│   ├── __init__.py               # Inicialización del módulo tests
│   ├── test_app.py                # Archivo con las pruebas
│── requirements.txt              # Dependencias de Python
│── employees.db                   # Base de datos SQLite
│── venv/                          # Entorno virtual (opcional)
```

---

## 🔧 Instalación y Configuración

### **1️⃣ Clonar el repositorio**
```sh
git clone https://github.com/CJGarCH/turia_tests.git
cd tu_carpeta
```

### **2️⃣ Configurar un entorno virtual**
#### Para macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

#### Para Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### **3️⃣ Instalar dependencias**
```sh
pip install -r requirements.txt
```

---

## ▶️ Ejecutar la Aplicación

### **Ejecutar el servidor Flask**
```sh
python app/app.py
```
La API estará disponible en:
```
http://127.0.0.1:5000
```

Puedes verificar con:
```sh
curl -X GET http://127.0.0.1:5000/employees
```

---

## 📖 Documentación con Swagger

Una vez que el servidor esté corriendo, accede a la documentación interactiva en:
```
http://127.0.0.1:5000/apidocs/
```

---

## 🔬 Pruebas Automatizadas

Para ejecutar las pruebas con `pytest`:
```sh
pytest tests/test_app.py -v
```

Si estás en **macOS/Linux** y pytest no se encuentra, usa:
```sh
python3 -m pytest tests/test_app.py -v
```

Si `pytest` no está instalado, instálalo con:
```sh
pip install pytest
```

---

## 📌 Endpoints

### **1️⃣ Crear un Empleado**
`POST /employees`
```json
{
  "name": "Daniel",
  "position": "Backend Engineer",
  "salary": 1200
}
```

### **2️⃣ Obtener Todos los Empleados**
`GET /employees`

### **3️⃣ Obtener un Empleado por ID**
`GET /employees/{id}`

### **4️⃣ Actualizar un Empleado**
`PUT /employees/{id}`
```json
{
  "name": "Daniel",
  "position": "Senior Developer",
  "salary": 2000
}
```

### **5️⃣ Eliminar un Empleado**
`DELETE /employees/{id}`

---

## 📌 Contribuciones
Si deseas contribuir, haz un **fork** del repositorio, crea una nueva rama y envía un **pull request**. 🚀

## 📄 Licencia
MIT License - Eres libre de usar y modificar este código.

