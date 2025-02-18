# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy repository contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit runs on
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "api.py", "--server.port=8501", "--server.address=0.0.0.0"]