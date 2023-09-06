FROM python:3.11-alpine

WORKDIR /code

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

CMD ["python", "-m", "app.main"]