FROM ubuntu:16.04
MAINTAINER Dogukan Cagatay <dcagatay@gmail.com>

ADD ./ /twitter-siphon/
WORKDIR /twitter-siphon
EXPOSE "5000:5000"

RUN echo "deb http://downloads.skewed.de/apt/xenial xenial universe" >> /etc/apt/sources.list && \
	echo "deb-src http://downloads.skewed.de/apt/xenial xenial universe" >> /etc/apt/sources.list
RUN apt-key adv --keyserver pgp.skewed.de --recv-key 612DEFB798507F25
RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install --yes --no-install-recommends --allow-unauthenticated \
	python3-graph-tool=2.26-1
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV PYTHONPATH /twitter-siphon
CMD ["python3", "social_networks/network_controller/http_controller.py"]

