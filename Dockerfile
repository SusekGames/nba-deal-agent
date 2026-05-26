FROM mcr.microsoft.com/playwright/python:v1.60.0-noble

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]