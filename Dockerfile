FROM python:3.11-slim

WORKDIR /app

# Copy app and test files
COPY ./app ./app
COPY ./tests ./tests
COPY requirements.txt .
COPY test.db ./test.db

# Set Python path so FastAPI finds app.*
ENV PYTHONPATH=/app

# Install everything including httpx
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir httpx

# Run tests
RUN pytest tests --disable-warnings

# Final command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
