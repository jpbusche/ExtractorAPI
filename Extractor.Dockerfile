FROM python:3.6

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apt-get install curl

WORKDIR /home/ExtractorAPI

CMD ./extractor.sh