__author__ = 'sunnyday'
import simplejson
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from http import Http

logger = logging.getLogger(__name__)


class VirusTotalClient(object):
    URL = "https://www.virustotal.com/vtapi/v2/url"
    API_KEY = "a61de549cfa5da4f08006df54748a3e9b0b0b0b3343a24d41a931da8ab71d1de"
    SCANNING = 1
    RETRIEVING = 2

    def __init__(self):
        self.transfer = Http(url=self.URL)

    def check_url(self, url):
        val = URLValidator()
        try:
            val(url)
        except ValidationError, e:
            logger.exception('Url %s is incorrect', url)
            raise e

    def send(self, url, type=1):
        result = []
        if type == self.SCANNING:
            self.transfer.url = self.URL + '/scan'
            self.transfer.request_data = dict(url=url, apikey=self.API_KEY)
        elif type == self.RETRIEVING:
            self.transfer.url = self.URL + '/report'
            self.transfer.request_data = dict(resource=url, apikey=self.API_KEY)
        self.transfer.send()
        logger.debug('VirusTotal response: %s', self.transfer.response_data)
        result = simplejson.loads(self.transfer.response_data)
        return result