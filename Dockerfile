# Use the official Python image instead of AWS's custom image
FROM python:3.11 AS build-stage

# Set the working directory
WORKDIR /app

# Copy the repository files
COPY . /app

# Ensure pip is installed
RUN apt-get update && apt-get install -y python3-pip

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "api.py", "--server.port=8501", "--server.address=0.0.0.0"]