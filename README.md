# Sample Django Project to re-practice latest django features using django5

## Using simple DOCKERFILE

```dockerfile
    FROM python:3.11.5
    WORKDIR /usr/src/app
    COPY requirements.txt ./
    RUN pip install -r requirements.txt
    COPY ./src .
    EXPOSE 8000
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Running instructions

1. Build using `docker build --tag docker-django5 .`
2. Run it using `docker run -p 8000:8000  docker-django5`
3. Check your browser at `127.0.0.1/polls`
4. Done