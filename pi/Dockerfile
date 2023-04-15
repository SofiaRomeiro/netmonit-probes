FROM python:3.9.2

WORKDIR /pi

COPY requirements.txt requirements.txt

RUN pip install --upgrade -r requirements.txt

RUN apt-get install iperf3

COPY . .

CMD ["python", "-u", "./main.py"]

#CMD uvicorn main:app --host="0.0.0.0" --port=8082 --reload