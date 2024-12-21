# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pendulum

# Copy the project files
COPY . .

# Airflow entrypoint
CMD ["airflow", "webserver"]
