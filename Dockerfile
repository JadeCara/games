# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "games.api:app", "--host", "0.0.0.0", "--port", "8000"]
