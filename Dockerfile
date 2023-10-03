FROM ubuntu:22.04
WORKDIR /home/ubuntu
RUN apt update
RUN apt install -y sudo
RUN sudo apt install -y python3
RUN sudo apt install -y python3-pip
RUN sudo apt-get install -y pkg-config
RUN command sudo apt -y install libmysqlclient-dev
RUN sudo apt install -y mysql-server
RUN sudo apt install -y redis-server
RUN mv 6379.conf /etc/redis/
RUN redis-server /etc/redis/6379.conf
RUN redis-cli PING

# Set the MySQL root password
RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
# RUN ./start_sql_service
# RUN cat setupDatabase.sql | sudo mysql -uroot -proot
# RUN ./createRecipeDataDB.py
EXPOSE 9000
EXPOSE 9001

# CMD ["./start_servers"]
