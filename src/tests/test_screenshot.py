from unittest import TestCase
from unittest.mock import MagicMock
import screenshot
from screenshot import RuntimeException

class TestScreenshot(TestCase):

    def test_site_unacessible(self):
        screenshot.is_site_reacheable = MagicMock(return_value=False)
        with self.assertRaises(RuntimeException):
            screenshot.take_screenshot("http://fake.url")

    def test_image_already_exists(self):
        screenshot.is_site_reacheable = MagicMock(return_value=True)
        screenshot.get_url_content_hash = MagicMock(return_value="ausdsadashd")
        screenshot.get_image_url = MagicMock(return_value="aaaaaa")
        assert(screenshot.take_screenshot("http://fake.url"), "aaaaaa")
    
    def test_screenshot_successful(self):
        screenshot.is_site_reacheable = MagicMock(return_value=True)
        screenshot.get_url_content_hash = MagicMock(return_value="ausdsadashd")
        screenshot.get_image_url = MagicMock(return_value="")
        screenshot.selenium_screenshot = MagicMock(return_value=True)
        screenshot.upload_to_bucket = MagicMock(return_value="http://fake.bucket.url")
        
        assert(screenshot.take_screenshot("http://fake.url"), "http://fake.bucket.url")
    
