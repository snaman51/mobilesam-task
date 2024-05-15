FROM python:3.9-slim

RUN apt-get update && apt-get install -y git libgl1-mesa-glx libglib2.0-0

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
