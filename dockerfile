# Use a Python base image in version 3.8
FROM python:3.8

# Set the working directory
WORKDIR /project

# Copy the application files to the container
COPY . /project

# Expose the application port 3111
EXPOSE 3111

# Install packages defined in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Initialize the database with pre-defined posts
RUN python init_db.py

# Set the command to execute when the container starts
CMD ["python", "app.py"]
