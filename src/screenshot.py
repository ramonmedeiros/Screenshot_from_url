from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from google.cloud.storage import Client
from PIL import Image

import imagehash
import log
import requests
import os
import tempfile

logger = log.getLogger()
log.set_verbosity(log.INFO)

def take_screenshot(url):
    image_file = "%s.png" % tempfile.mktemp()

    if is_site_reacheable(url) == False:
        logger.info("%s not reacheable" % url)
        return False

    logger.info("screenshot for %s" % url)
 
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # start webdriver
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)

        element = driver.find_element_by_tag_name('body')
        element_png = element.screenshot_as_png
        with open(image_file, "wb") as file:
            file.write(element_png)

        driver.quit()

    except Exception as e:
        logger.info("Problem with screenshot" + str(e))
        return "error while screenshot " 


    try:
        image_url = upload_to_bucket(image_file)
    except Exception as e:
        logger.info("Problems while uploading image: " + str(e))
        return "Problems while uploading image: " + str(e)

    finally:
        if os.path.exists(image_file):
            os.remove(image_file)

    return image_url

def is_site_reacheable(url):

    req = requests.head(url)
    return req.status_code < 400

def upload_to_bucket(filename):
    if os.path.exists(filename) is False:
        logger.info("File %s does not exists" % filename)
        return false

    imageHsh = str(imagehash.phash(Image.open(filename)))

    client = Client()
    bucket = client.get_bucket("detectifychallengeramon")

    # check if screenshot already exists
    for blob in bucket.list_blobs():
        if imageHsh == blob.name:
            logger.info("Image %s already exists" % imageHsh)
            return blob.public_url

    logger.info("new image. Uploading screenshot")
    blob = bucket.blob(imageHsh)
    blob.upload_from_filename(filename)
    
    # make public and return url
    blob.make_public()
    logger.info("Screenshot at %s" % blob.public_url)
    return blob.public_url

