FROM python:3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apk add --no-cache curl \
 && pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir fastapi uvicorn
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/
RUN chown -R 1000:0 /app
USER 1000:1000
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
