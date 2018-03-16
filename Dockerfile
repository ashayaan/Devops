FROM ashayaan/flask-server

MAINTAINER Name Shayaan_Pranav
RUN rm -rf Devops
RUN git clone https://github.com/ashayaan/Devops.git
EXPOSE 5000
WORKDIR Devops
CMD python Devops/server.py &