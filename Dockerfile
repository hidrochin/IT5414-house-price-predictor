FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching  
COPY src/api/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source code
COPY src/api/*.py ./

# Copy model files
COPY models/trained/*.pkl ./models/trained/

# Expose port
EXPOSE 8000

# Run API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
