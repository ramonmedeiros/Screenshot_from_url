import hashlib
import magic
import pub
import threading

from unittest import TestCase
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pub import RuntimeException

EXPECTED_HASH = "7fffffffffffffff"


class TestScreenshot(TestCase):

    def setUp(self):
        server_address = ('', 0)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        self.port = httpd.server_port
        self.server = threading.Thread(target=httpd.serve_forever, daemon=True)
        self.server.start()

    def test_screenshot_successful(self):
        content = pub.selenium_screenshot(
            f"http://127.0.0.1:{self.port}/src/tests/mocks/")
        assert(pub.get_image_hash(content) == EXPECTED_HASH)

    def teardown(self):
        self.server.exit()
