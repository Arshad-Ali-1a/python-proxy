FROM python:3.10
LABEL authors="Arshad Ali"

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 9002
CMD ["python", "app.py"]
