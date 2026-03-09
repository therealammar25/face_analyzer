# Official Python slim image (small aur fast)
FROM python:3.11-slim

# Working directory set karo
WORKDIR /app

# Pehle requirements copy aur install (fast caching ke liye)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki project copy karo
COPY . .

# Port expose (Render $PORT use karega)
EXPOSE 8000

# App start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]