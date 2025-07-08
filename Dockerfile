# 1. Use a lightweight Python image as the base
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy all backend files (app.py, .env, requirements.txt, etc.)
COPY . .


# 4. Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose FastAPI’s default port
EXPOSE 8000

# 6. Run your FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
