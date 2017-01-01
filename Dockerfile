FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN useradd ciupy3

ADD requirements.txt /app/
RUN pip install -r requirements.txt

RUN chown -R ciupy3:ciupy3 /app
USER ciupy3

ADD . /app/

CMD ["python", "manage.py", "runserver"]
