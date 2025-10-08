# Use Python 3.10 as base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose Django default port
EXPOSE 8000

# Command to run the Django server
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 -p 8000"]
