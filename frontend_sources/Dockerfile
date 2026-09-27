
# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy frontend files into the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Start the Streamlit application
CMD ["streamlit", "run", "superkart_sales_app_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
