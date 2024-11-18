FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["sh", "-c", "python init_db.py & python mqtt_client.py & python app.py"]
