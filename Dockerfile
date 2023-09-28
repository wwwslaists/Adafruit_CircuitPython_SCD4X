FROM arm32v7/python:3

# We copy just the requirements.txt first to leverage cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

COPY examples/ /app

EXPOSE 5000

ENTRYPOINT ["python3", "-u", "main.py"]