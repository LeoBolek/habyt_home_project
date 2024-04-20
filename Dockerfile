# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Download the repository from GitHub
RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/LeoBolek/habyt_home_project.git /app/habyt-rental-system

# Set the working directory to the cloned repository
WORKDIR /app/habyt-rental-system

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/habyt-rental-system
COPY . .

# Run the Python script
CMD [ "python", "./pipeline.py" ]
