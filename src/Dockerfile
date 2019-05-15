FROM python:3.7

# install pip
RUN apt-get update
RUN apt-get install python-pip wkhtmltopdf xvfb -y

# set path to selenium files (selenium jar and chromedriver)
ENV PYTHONPATH="/app/"
ENV FLASK_APP="/app/service.py"
ENV FLASK_ENV="production"
ENV DISPLAY=:99.0

# copy files 
WORKDIR /app
COPY * /app/

# install requirements
RUN pip install -r /app/requirements.txt

EXPOSE 8080

# entrypoint
CMD ["/app/entry_point.sh"]
