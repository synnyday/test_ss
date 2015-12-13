# -*- coding: utf-8 -*-
"""
Command to check urls
"""
import logging
import csv
import sys
import simplejson

from base import BaseCommand
from test_ss.virustotal_client import VirusTotalClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    u"""
    класс команды проверки urls
    """
    urls = [
        'http://www.stellarium.org',
        'http://icloud-iosid.win/',
        # 'fffg'
        ]
    client = ''

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--urls', type=str, default=None,
                            help='Use comma-separated URLs list (priority option)')
        parser.add_argument('--file', type=str, default=None,
                            help='Path to csv file with URLs (the URLs must be separated by a new line character)')

    def process(self, *args, **options):
        """
        Get additional options and check URLs
        :param args:
        :param options:
        :return:
        """
        if options['urls'] is not None:
            self.urls = [str(it) for it in options['urls'].split(',')]
        elif options['file'] is not None:
            try:
                # TODO Validation entities from file
                self.urls = [line.rstrip('\n') for line in open(options['file'])]
            except:
                logger.exception('Error read csv file %s', options['file'])
                sys.exit('Error read csv file')
        self.client = VirusTotalClient()
        self._check_urls()
        response = self.submit_batch_for_scanning()
        reports = self._retrieving_url_scan_reports(response)
        sites = self.get_phishing_urls(reports)
        if sites:
            print "Phishing sites: \n{}" . format(sites),
        else:
            print 'Phishing sites not found'

    def submit_batch_for_scanning(self):
        result = list()
        batch = '\n' . join(self.urls)
        try:
            result = self.client.send(batch)
            if not result:
                raise Exception("Response is empty")
        except:
            logger.exception("Error to submit batch for scanning: %s", batch)
            sys.exit("Error to submit URLs for scanning")
        return result

    def _check_urls(self):
        for url in self.urls:
            try:
                self.client.check_url(url)
            except:
                self.urls.remove(url)
                logger.error("URL have been skipped: %s", url)
        if self.urls.__len__() < 1:
            sys.exit('List URLs is empty')
        else:
            logger.debug("Check current urls: %s",  self.urls)

    def _retrieving_url_scan_reports(self, retrieving_urls):
        """
        URLs sent using the API have the lowest scanning priority,
        depending on VirusTotal's load,
        it may take several hours before the URL is scanned
        :param retrieving_urls:
        :return: Retrieving URLs scan reports
        """
        print "Start to retrieving URLs scan reports"
        reports = list()
        # TODO Need to send query the report at regular intervals until the result shows up
        # while(retrieving_urls.__len__() > 0):
        for retrieving_url in retrieving_urls:
            if 'response_code' not in retrieving_url or retrieving_url['response_code'] == 0:
                logger.error('The response code does not exist or item was not present in VirusTotal dataset')
                # retrieving_urls.remove(retrieving_url)
                continue
            if retrieving_url['response_code'] == -2:
                logger.error('Url is still queued for analysiss')
                continue
            if 'resource' not in retrieving_url:
                logger.error('The resource does not exist')
                # retrieving_urls.remove(retrieving_url)
                continue
            if retrieving_url['resource'] not in self.urls:
                logger.error('URL not found in the check list: %s', retrieving_url['resource'])
                # retrieving_urls.remove(retrieving_url)
                continue
            logger.debug("Retrieving current url: %s",  retrieving_url['resource'])
            try:
                report = self.client.send(retrieving_url['resource'], 2)
                if 'response_code' in retrieving_url and retrieving_url['response_code'] == 1:
                    reports.append(report)
                    # retrieving_urls.remove(retrieving_url)
            except:
                logger.exception("Error to submit resource for retrieving: %s", retrieving_url['resource'])
        return reports

    def get_phishing_urls(self, reports):
        """
        Filtering urls
        :return: list of urls with phishing scam
        """
        phishing_urls = list()
        for report in reports:
            if 'scans' not in report:
                logger.error('Scanning information not found')
                continue
            for name, scan in report['scans'].iteritems():
                if 'result' not in scan:
                    logger.error('%s result scanning not found', name)
                    continue
                if scan['result'] == 'phishing site':
                    phishing_urls = report['url']
                    break
        return phishing_urls
