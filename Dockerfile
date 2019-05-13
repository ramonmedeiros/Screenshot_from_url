FROM selenium/standalone-chrome

RUN sudo apt-get update
RUN sudo apt-get install python-pip -y

WORKDIR /app
COPY * /app/
RUN pip install -r /app/requirements.txt

