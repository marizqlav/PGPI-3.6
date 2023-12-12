FROM python:3.10-alpine3.16

ENV PYTHONUNBUFFERED = 1 
ENV PYTHONDONTWRITEBYTECODE = 1

WORKDIR /app

RUN apk add --update git
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base
RUN apk add --virtual build-deps gcc python3-dev musl-dev

RUN pip install gunicorn
RUN pip install ipdb
RUN pip install ipython

RUN pip install Django==3.0.14
RUN pip install Pillow==9.3.0
RUN pip install stripe==2.63.0
RUN pip install django-material-admin
RUN pip install python-dateutil
RUN pip install djangorestframework


RUN mkdir /app/ecommerce

RUN git clone https://github.com/marizqlav/PGPI-3.6.git /app/ecommerce

COPY . .

CMD ["python", "manage.py" , "runserver", "0.0.0.0:5000"]
