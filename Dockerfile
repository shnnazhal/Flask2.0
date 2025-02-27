# Start with a Python base image
FROM python:3.9-slim

# The /app directory will act as the main application directory
WORKDIR /app

# Copy requirements file (if you have one)
# If not, create one with Flask dependency: echo "Flask==2.0.1" > requirements.txt
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application files
COPY ./app.py ./
COPY ./templates ./templates
# Add any other files or directories your Flask app needs

# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
