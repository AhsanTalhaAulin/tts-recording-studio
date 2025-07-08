# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the backend directory into the container
COPY backend /app/backend

# Create the data directory for persistent storage
RUN mkdir -p /app/data

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
# Use --host 0.0.0.0 to make it accessible from outside the container
# Use --reload for hot-reloading during development (useful with mounted volumes)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
