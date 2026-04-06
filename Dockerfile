FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose required port
EXPOSE 7860

# Start FastAPI server (MAIN ENTRYPOINT)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]