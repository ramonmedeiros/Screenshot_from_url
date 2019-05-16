from unittest import TestCase
from unittest.mock import MagicMock

import service


class TestService(TestCase):

    def setUp(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()

    def test_invalid_url(self):
        # not being able to create test instance
        pass
        #rv = self.app.post("/screenshot", json={"url": "http://string"})
        #assert(rv.status_code == 500)
        #assert(rv.get_json()["message"] == "connection error to url http://string")
