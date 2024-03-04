# Use the official Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app



RUN pip install Flask
RUN pip install Jinja2
RUN pip install requests

# Copy the application code
COPY FS.py .

# Expose the port on which the application will run
EXPOSE 9090

# Command to run the application
CMD ["python", "FS.py"]