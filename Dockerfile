FROM selenium/standalone-chrome

# install pip
RUN sudo apt-get update
RUN sudo apt-get install python-pip -y

# set path to selenium files (selenium jar and chromedriver)
ENV PATH="/opt/selenium/:/opt/google/:/opt/google/chrome:${PATH}"
ENV PYTHONPATH="/app/"
ENV FLASK_APP="/app/service.py"
ENV FLASK_ENV="development"

# copy files 
WORKDIR /app
COPY * /app/

# TODO: use kubernetes secrets
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/detectify-challenge-ramon-24b9a8ef7c2a.json
COPY detectify-challenge-ramon-24b9a8ef7c2a.json /app/

# install requirements
RUN pip install -r /app/requirements.txt

EXPOSE 5000

# entrypoint
CMD ["/home/seluser/.local/bin/flask" ,"run", "--host=0.0.0.0"]
