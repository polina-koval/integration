FROM python:3.12-slim

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --default-timeout=100 -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["python3", "manage.py"]
CMD ["service"]