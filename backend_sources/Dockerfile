
# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy backend files into the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask backend port
EXPOSE 7860

# Start the Flask API using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
