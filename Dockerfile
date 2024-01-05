FROM python:3.11.5
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
WORKDIR /usr/src/app/src
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]