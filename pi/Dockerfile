FROM python:3.9.2

WORKDIR /pi

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "./main.py"]