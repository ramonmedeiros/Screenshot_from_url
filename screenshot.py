from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from uuid import uuid4
from google.cloud.storage import Client

import log
import requests
import os

logger = log.getLogger()
log.set_verbosity(log.INFO)
IMAGE = "my_screenshot.png"
DRIVER = 'chromedriver'

def take_screenshot(url):
    if is_site_reacheable(url) == False:
        return False

    logger.info("screenshot for %s" % url)
 
    try:
        driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
        driver.get(url)

        # TODO: its possible to receive the base64 instead file 
        screenshot = driver.save_screenshot(IMAGE)
        driver.quit()
    except Exception as e:
        print "Problem with selenium" + str(e)

    try:
        upload_to_bucket(IMAGE)
    except Exception as e:
        print "Problems while uploading image: " + str(e)
    finally:
        os.remove(IMAGE)

def is_site_reacheable(url):

    req = requests.head(url)
    return req.status_code == 200

def upload_to_bucket(filename):
    if os.path.exists(filename) is False:
        print "File %s does not exists" % filename

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

take_screenshot("http://www.google.com")
