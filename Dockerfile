# FROM python:3.10-slim-buster
# WORKDIR /app
# COPY . /app

# RUN apt update -y && apt install awscli -y

# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 unzip -y && pip install -r requirements.txt
# CMD ["python3", "app.py"]


FROM python:3.10-slim

WORKDIR /app
COPY . /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 unzip -y && pip install -r requirements.txt



CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
