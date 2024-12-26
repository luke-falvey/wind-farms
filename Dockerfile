FROM python:3.12-slim
RUN apt-get update && apt-get upgrade && rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
RUN pip install --user --no-cache -r requirements.txt && rm requirements.txt
COPY src/ .
CMD [ "python", "main.py"]