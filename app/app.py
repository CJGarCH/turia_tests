from flask import Flask, request, jsonify
from flasgger import Swagger
import sqlite3

app = Flask(__name__)
swagger = Swagger(app)

# Ruta de la base de datos local
DB_PATH = "employees.db"

# Crear la base de datos y la tabla si no existen
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL
            )
        """)
        conn.commit()

init_db()  # Se ejecuta al iniciar el servidor

def validate_employee(data):
    """Valida los campos requeridos del empleado."""
    if "name" not in data or not isinstance(data["name"], str) or not data["name"].strip():
        return "Invalid name"
    if "position" not in data or not isinstance(data["position"], str) or not data["position"].strip():
        return "Invalid position"
    if "salary" not in data or not isinstance(data["salary"], (int, float)) or data["salary"] <= 0:
        return "Invalid salary"
    return None

@app.route("/employees", methods=["POST"])
def create_employee():
    """
    Crea un nuevo empleado.
    ---
    tags:
      - Employees
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Employee
          required:
            - name
            - position
            - salary
          properties:
            name:
              type: string
              example: "Carlos Pérez"
            position:
              type: string
              example: "Backend Engineer"
            salary:
              type: number
              example: 5000
    responses:
      201:
        description: Empleado creado exitosamente
      400:
        description: Datos inválidos
    """
    data = request.get_json()
    error = validate_employee(data)
    if error:
        return jsonify({"error": error}), 400

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", 
                       (data["name"], data["position"], data["salary"]))
        conn.commit()
        employee_id = cursor.lastrowid

    return jsonify({"id": employee_id}), 201

@app.route("/employees", methods=["GET"])
def list_employees():
    """
    Obtiene la lista de todos los empleados.
    ---
    tags:
      - Employees
    responses:
      200:
        description: Lista de empleados
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, position, salary FROM employees")
        employees = [{"id": row[0], "name": row[1], "position": row[2], "salary": row[3]} for row in cursor.fetchall()]

    return jsonify(employees), 200

@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    """
    Obtiene un empleado por ID.
    ---
    tags:
      - Employees
    parameters:
      - name: employee_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Datos del empleado
      404:
        description: Empleado no encontrado
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, position, salary FROM employees WHERE id = ?", (employee_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({"error": "Employee not found"}), 404

    return jsonify({"id": row[0], "name": row[1], "position": row[2], "salary": row[3]}), 200

@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    """
    Actualiza un empleado por ID.
    ---
    tags:
      - Employees
    parameters:
      - name: employee_id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          id: EmployeeUpdate
          properties:
            name:
              type: string
              example: "Carlos Pérez"
            position:
              type: string
              example: "Senior Developer"
            salary:
              type: number
              example: 6000
    responses:
      200:
        description: Empleado actualizado exitosamente
      400:
        description: Datos inválidos
      404:
        description: Empleado no encontrado
    """
    data = request.get_json()
    error = validate_employee(data)
    if error:
        return jsonify({"error": error}), 400

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET name = ?, position = ?, salary = ? WHERE id = ?", 
                       (data["name"], data["position"], data["salary"], employee_id))
        if cursor.rowcount == 0:
            return jsonify({"error": "Employee not found"}), 404
        conn.commit()

    return jsonify({"message": "Employee updated successfully"}), 200

@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    """
    Elimina un empleado por ID.
    ---
    tags:
      - Employees
    parameters:
      - name: employee_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Empleado eliminado exitosamente
      404:
        description: Empleado no encontrado
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Employee not found"}), 404
        conn.commit()

    return jsonify({"message": "Employee deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
