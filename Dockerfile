# Use an official Python runtime as a parent image
FROM python:3.9.6-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY *.py requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for Streamlit to run on Cloud Run
ENV STREAMLIT_SERVER_PORT=8080

# Set the streamlit command to run the app
ENTRYPOINT ["streamlit", "run", "app.py"]