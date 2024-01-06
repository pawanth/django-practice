FROM python:3.11.5
WORKDIR /usr/src/code
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y build-essential net-tools curl wget git nano ssh iputils-ping htop tree

COPY requirements.txt ./
RUN pip install --user -U -r requirements.txt

SHELL ["/bin/bash", "--login", "-c"]
CMD ["bash"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]