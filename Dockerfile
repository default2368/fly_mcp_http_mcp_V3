FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia i file dell'applicazione
COPY main.py .
COPY config.py .

# Installa psutil per system stats
RUN pip install psutil

CMD ["python", "main.py"]
