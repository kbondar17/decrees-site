FROM python:3.10
WORKDIR /my_project    
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5544
CMD [ "python3", "myapp.py"]
CMD [ "python3", "app/manage.py", "runserver", "0.0.0.0:7000"]

