Sample django project to practice revisit each upgrade of django with all test stuff available on django official website

## Using simple DOCKERFILE

```dockerfile
    # Dockerfile
    FROM python:3.11.5
    WORKDIR /usr/src/app
    COPY requirements.txt ./
    RUN pip install -r requirements.txt
    COPY . .
    EXPOSE 8000
    WORKDIR /usr/src/app/src
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```dockerfile
    # docker-compose
    version: "3.9"
    services:
        django:
            build: .
            environment:
                - SECRET_KEY=23408728djlkjd37nmckdllsorhh377889s900&
            ports:
                - "8000:8000"
```

## Running instructions

1. Build using `docker-comose build`
2. Run it using `docker-compose up`
3. Check your browser at `127.0.0.1/polls`
4. Done

## Other userful docker-compose commands
- `docker-compose down` # Delete the associated containers
- `docker-compose run --rm web bash` # directly open the bas on web service
- `docker-compose exec web bash` # Exec/ssh into running docker service
