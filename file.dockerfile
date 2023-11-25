# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
# This includes Flask and any other libraries your app needs (like requests, pandas, matplotlib)
RUN pip install Flask requests pandas matplotlib

# Make port 5000 available to the world outside this container
# This is the default port that Flask runs on
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
