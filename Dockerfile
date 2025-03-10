# Usa una imagen ligera de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia y instala las dependencias antes de copiar el código
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . /app

# Expone el puerto 5000
EXPOSE 5010

# Comando para ejecutar la aplicación de forma normal
CMD ["python", "app/app.py"]