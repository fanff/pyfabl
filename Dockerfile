FROM ubuntu:14.04
MAINTAINER Fanf <fanf@fanf>
RUN apt-get update && apt-get -y install vim socat man 
RUN apt-get update && apt-get -y install python-pip 
RUN pip install twisted
