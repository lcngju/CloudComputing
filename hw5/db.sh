#!/bin/bash
docker pull mongo:latest
docker run -itd --name mongo -p 27017:27017 mongo
python3 -m pip3 install pymongo
