import os
import log
import json
import random
import string
import time
import sys
import base64

from io import BytesIO
from google.cloud import pubsub_v1
from utils import RuntimeException, get_bucket

logger = log.getLogger()
log.set_verbosity(log.INFO)

# get bucket name from environment
BUCKET = os.environ.get("GCS_BUCKET")
PROJECT = os.environ.get("GCP_PROJECT")
TOPIC = os.environ.get("GCP_TOPIC")
SUB_PATH = ""


def upload_to_bucket(imageContent, imageHash):

    try:
        bucket = get_bucket(BUCKET)
        logger.info("new image. Uploading screenshot")
        blob = bucket.blob(imageHash)
        blob.upload_from_file(BytesIO(base64.b64decode(
            imageContent)), content_type="image/png")

        # make public and return url
        blob.make_public()
    except Exception as e:
        raise RuntimeException(
            f"Problems while uploading screenshot. {str(e)}")

    logger.info(f"Screenshot at {blob.public_url}")
    return blob.public_url


def create_subscription():
    """Create a new pull subscription on the given topic."""
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(PROJECT, TOPIC)
    global SUB_PATH
    name = ''.join(random.choice(string.ascii_lowercase) for i in range(9))
    SUB_PATH = subscriber.subscription_path(
        PROJECT, name)

    subscription = subscriber.create_subscription(
        SUB_PATH, topic_path)

    return subscription


def receive_messages():
    """Receives messages from a pull subscription."""
    create_subscription()
    subscriber = pubsub_v1.SubscriberClient()

    def callback(message):
        sys.stdout.write(f'Received message: ')
        msg = json.loads(message.data.decode())
        upload_to_bucket(msg["image"], msg["imageHash"])
        message.ack()

    subscriber.subscribe(SUB_PATH, callback=callback)
    print(f'Listening for messages on {SUB_PATH}')
    while True:
        time.sleep(60)
