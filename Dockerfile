# Use the official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Cloud Run default)
EXPOSE 5000

# Set environment variable for Flask
ENV PORT=5000
ENV FLASK_APP=app.py

# Run the Flask app
CMD ["gunicorn", "-b", ":5000", "app:app"]
