FROM ubuntu:16.04

MAINTAINER Name Shayaan_Pranav
RUN apt-get -y update
RUN apt-get -y install python-pip git
RUN pip install flask
RUN git clone https://github.com/ashayaan/Devops.git
#RUN cd Devops
EXPOSE 5000
CMD python Devops/server.py &