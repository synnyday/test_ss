# -*- coding: utf-8 -*-
u"""
базовая команда
"""
import logging
from django.core.management.base import BaseCommand as DjangoBaseCommand
from django.core.management import CommandError
from django.utils import translation
from django.conf import settings

__all__ = ['BaseCommand', 'CommandError']

logger = logging.getLogger(__name__)

class BaseCommand(DjangoBaseCommand):
    u"""
    базовая команда
    """

    def handle(self, *args, **options):
        logger.info('command %s started', type(self).__module__.split('.')[-1])
        translation.activate(settings.LANGUAGE_CODE)
        try:
            result = self.process(*args, **options)
        except Exception as ex:
            logger.exception(ex)
            result = None
        logger.info('command %s completed', type(self).__module__.split('.')[-1])
        return result

    def process(self, *args, **options):
        raise NotImplementedError('This is an abstact base command')