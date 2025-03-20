# Use the official Python 3.9 image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Set the Python module search path to include the backend directory
ENV PYTHONPATH="/app:/app/backend"

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the wait-for-it.sh script into the container (if not already in your project root)
COPY wait-for-it.sh /app/wait-for-it.sh

# Make the wait-for-it.sh script executable
RUN chmod +x /app/wait-for-it.sh

# Command to run the application (updated to reference the backend module)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]