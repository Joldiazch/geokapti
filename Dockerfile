# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requisitos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente al directorio de trabajo
COPY . .

# Expone el puerto 8000 para la API
EXPOSE 8000

# Ejecuta el comando para iniciar la aplicación
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
