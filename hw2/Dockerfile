FROM jjanzic/docker-python3-opencv
ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

CMD ["python", "web_picture.py"]
