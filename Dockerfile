FROM python:3.10-bullseye

WORKDIR app
ENV FLASK_APP=app

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["flask", "--debug", "run", "--host=0.0.0.0"]
