FROM python:latest
ADD app /app
COPY startup.sh /
COPY backup.sql /
RUN chmod +x /startup.sh
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt update 
RUN apt install -y mariadb-server 
RUN mkdir -p /run/mysqld

ENTRYPOINT ["bash"]
CMD ["/startup.sh"]
