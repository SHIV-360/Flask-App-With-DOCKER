# use official python image
from python:3.12-slim

# set working directory inside container
workdir /app

# copy files into container
copy . /app

# install dependencies
run pip install flask psycopg2-binary

# expose flask port
expose 5000

# run app
cmd ["python", "main.py"]
