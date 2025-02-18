# Use an official Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Ensure Streamlit is installed
RUN pip show streamlit || pip install streamlit

# Expose the Streamlit default port
EXPOSE 8501

# Run the Streamlit application
CMD ["python3", "-m", "streamlit", "run", "api.py", "--server.port=8501", "--server.address=0.0.0.0"]