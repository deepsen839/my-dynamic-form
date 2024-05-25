# Use the official Python image from the Docker Hub
FROM python:3.12.3-slim-bullseye

# Set the working directory
WORKDIR /module

# Copy the requirements file into the image
COPY requirements.txt .

# Install dependencies required to build mysqlclient
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential pkg-config && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for the app
EXPOSE 8000

# Run the Django server
CMD ["sh", "-c", "python3 manage.py migrate --noinput && python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:8000"]
