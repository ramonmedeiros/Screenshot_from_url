from google.cloud.storage import Client

import log

logger = log.getLogger()
log.set_verbosity(log.INFO)


class RuntimeException(Exception):
    status_code = 500

    def __init__(self, message, image_file="", status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        logger.info(message)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def get_bucket(bucket):
    client = Client()
    return client.get_bucket(bucket)
