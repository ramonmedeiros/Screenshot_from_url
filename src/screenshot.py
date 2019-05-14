from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from uuid import uuid4
from google.cloud.storage import Client

import log
import requests
import os

logger = log.getLogger()
log.set_verbosity(log.INFO)
IMAGE = "/tmp/my_screenshot.png"

def take_screenshot(url):
    if is_site_reacheable(url) == False:
        logger.info("%s not reacheable" % url)
        return False

    logger.info("screenshot for %s" % url)
 
    try:

        # enforce headless
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # start webdriver
        driver = webdriver.Chrome(chrome_options=options)
        driver.maximize_window()
        driver.get(url)

        # TODO: its possible to receive the base64 instead file 
        screenshot = driver.save_screenshot(IMAGE)
        driver.quit()
    except Exception as e:
        logger.info("Problem with selenium" + str(e))

    try:
        image_url = upload_to_bucket(IMAGE)
    except Exception as e:
        logger.info("Problems while uploading image: " + str(e))
    finally:
        os.remove(IMAGE)

    return image_url

def is_site_reacheable(url):

    req = requests.head(url)
    return req.status_code < 400

def upload_to_bucket(filename):
    if os.path.exists(filename) is False:
        logger.info("File %s does not exists" % filename)
        return false

    client = Client()
    bucket = client.get_bucket("detectifychallengeramon")

    # creating md5 basic. Can use image fingerprinting
    logger.info("uploading screenshot")
    blob = bucket.blob(uuid4().__str__())
    blob.upload_from_filename(filename)
    
    # make public and return url
    blob.make_public()
    logger.info("Screenshot at %s" % blob.public_url)
    return blob.public_url

