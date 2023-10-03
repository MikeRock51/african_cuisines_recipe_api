FROM ubuntu:22.04
WORKDIR /home/ubuntu
COPY requirements.txt .
RUN sudo apt update
RUN sudo apt install python3
RUN sudo apt install python3-pip
RUN sudo apt-get install pkg-config
RUN command sudo apt-get install libmysqlclient-dev
RUN pip3 install -r requirements.txt
RUN sudo apt install mysql-server
RUN sudo systemctl start mysql.service
COPY . .
RUN cat setupDatabase.sql | mysql
RUN ./createRecipeDataDB.py
EXPOSE 9000
EXPOSE 9001

CMD ["./start_servers"]
