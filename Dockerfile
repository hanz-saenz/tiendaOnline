FROM python:3.13

WORKDIR /tienda

COPY . /tienda/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]