FROM selenium/standalone-chrome

# install pip
RUN sudo apt-get update
RUN sudo apt-get install python-pip -y

# put chromedriver in PATH to run locally, not Remote
ENV PATH="/opt/selenium/:/opt/google/:/opt/google/chrome:${PATH}"

# Flask envs
ENV PYTHONPATH="/app/"
ENV FLASK_APP="/app/service.py"
ENV FLASK_ENV="production"

# copy files 
WORKDIR /app
COPY * /app/

# install requirements
RUN pip install -r /app/requirements.txt

EXPOSE 8080

# entrypoint
CMD ["/home/seluser/.local/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]

