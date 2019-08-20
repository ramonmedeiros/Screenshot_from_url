from google.cloud.storage import Client
from google.cloud import pubsub_v1
from utils import RuntimeException, get_bucket
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from chromedriver_binary import chromedriver_filename

import os
import json
import log
import time
import imagehash
import base64
from PIL import Image
from io import BytesIO
logger = log.getLogger()
log.set_verbosity(log.INFO)

# get bucket name from environment
BUCKET = os.environ.get("GCS_BUCKET")
PROJECT = os.environ.get("GCP_PROJECT")
TOPIC = os.environ.get("GCP_TOPIC")

# webdriver options
SELENIUM_OPTIONS = webdriver.ChromeOptions()
SELENIUM_OPTIONS.add_argument('headless')


def publish_messages(message, project_id=PROJECT, topic_name=TOPIC):
    """Publishes multiple messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    future = publisher.publish(topic_path, data=json.dumps(message).encode())
    return future.result()

def get_image_hash(content):
    with Image.open(BytesIO(base64.b64decode(content))) as fd:
        return imagehash.average_hash(fd).__str__()

def take_screenshot(url):

    content = selenium_screenshot(url)
    imageHash = get_image_hash(content)
    image_url = get_image_exists(imageHash)

    # image already downloaded: return link
    if len(image_url) != 0:
        return image_url
    publish_messages({"imageHash": imageHash, "image": content})

def get_image_exists(imageHash):
    # check if screenshot already exists
    bucket = get_bucket(BUCKET)
    for blob in bucket.list_blobs():
        if imageHash == blob.name:
            logger.info(f"Image {imageHash} already exists")
            return blob.public_url

    return ''

def selenium_screenshot(url):
    logger.info(f"taking screenshot for {url}")
    
    # start webdriver
    driver = webdriver.Chrome(executable_path=chromedriver_filename, options=SELENIUM_OPTIONS)
    try:
        driver.set_window_size("1920", "2560")
        driver.get(url)
        content = driver.get_screenshot_as_base64()
    finally:
        driver.quit()

    return content

