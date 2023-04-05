FROM python:3.9.2

WORKDIR /pi

COPY requirements.txt requirements.txt

RUN pip install --upgrade -r requirements.txt

COPY . .

#CMD ["python", "-u", "./main.py"]
#CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8082", "--reload", "True", "main:app"]

CMD uvicorn main:app --host="0.0.0.0" --port=8082 --reload