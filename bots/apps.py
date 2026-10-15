# -*- coding: utf-8 -*-
"""
Bots django app config
"""

from django.apps import AppConfig

from . import __about__ as about


class Config(AppConfig):
    """Django app config"""
    # pylint: disable=too-few-public-methods
    name = __package__
    verbose_name = about.__summary__
    # keys stay 32 bit, as in the databases made by bots 3 (and no pending migration on newer django)
    default_auto_field = 'django.db.models.AutoField'
