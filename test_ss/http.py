# -*- coding: utf-8 -*-
__author__ = 'sunnyday'

import urllib2
import urllib
import logging
from httplib import BadStatusLine

logger = logging.getLogger(__name__)


class Http(object):
    request_data = ''
    response_data = ''

    def __init__(self, url, timeout=25):
        self.url = url
        self.timeout = timeout

    def send(self):
        request = urllib2.Request(self.url)
        request.add_data(urllib.urlencode(self.request_data))
        try:
            self.response_data = urllib2.urlopen(request, timeout=self.timeout)
            self.response_data = self.response_data.read()
        except BadStatusLine as e:
            error_response_data = "{0} {1}\n{2}\n{3}".format(e.code, e.reason, e.hdrs, e.read())
            logger.exception("Bad Status Line %s", error_response_data)
            raise Exception('Timeout error', previous=e)
        except urllib2.HTTPError as e:
            error_response_data = "{0} {1}\n{2}\n{3}".format(e.code, e.reason, e.hdrs, e.read())
            logger.exception("HTTPError %s", error_response_data)
            raise Exception('Error response received', previous=e)
        except urllib2.URLError as e:
            logger.exception('URLError %s', e.reason)
            raise Exception('Nothing matches the given URI')