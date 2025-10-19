FROM python:3.13-alpine
WORKDIR /app
RUN chown -R 1000:0 /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/
USER 1000:1000
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
