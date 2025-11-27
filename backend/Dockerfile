# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application using Uvicorn
# 0.0.0.0 is required for the container to be accessible from outside
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]