FROM python:3.9

ADD WeatherCollection.py .

RUN pip install pymongo
RUN pip install datetime
RUN pip install pandas

CMD ["python", "./WeatherCollection.py"]


