# Usa una imagen de Python ligera
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Permitir que Flask recargue automáticamente
ENV FLASK_ENV=development

# Expone el puerto en el que Flask correrá
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "run.py"]
