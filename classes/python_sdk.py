# -*- coding: utf-8 -*-
"""Class to handle AWS SDK for Python - Boto3."""

import os
import sys

from logging import getLogger
from boto3 import Session
from botocore.credentials import JSONFileCache
from botocore.exceptions import ProfileNotFound, ClientError

DEFAULT_REGION = 'ap-southeast-2'
MODULE_LOGGER = getLogger(__name__)


class AwsSession:  # pylint: disable=R0903
    """Manage boto3 session."""
    _class_logger = MODULE_LOGGER.getChild(__qualname__)

    def __init__(self, profile: str, region=DEFAULT_REGION, authentication='sso') -> None:
        """Initialize class."""
        self._instance_logger = self._class_logger.getChild(str(id(self)))
        self.profile = profile
        self.region = region
        if authentication == 'sso' or authentication == 'cli':  # pylint: disable=R1714
            self.authentication = authentication
        else:
            self._instance_logger.error(
                'Allowed values for authentication variable are sso or cli.'
            )
            sys.exit(-1)

    def cli(self):
        """Start a session to be used from CLI."""
        cache = f".aws/{self.authentication}/cache"

        cli_cache = os.path.join(os.path.expanduser('~'), cache)
        cli_session = None
        try:
            cli_session = Session(
                profile_name=self.profile,
                region_name=self.region
            )

        except ProfileNotFound as e:
            self._instance_logger(e)
            sys.exit(-1)

        cli_session._session.get_component(  # pylint: disable=W0212
            'credential_provider'
        ).get_provider(
            'assume-role'
        ).cache = JSONFileCache(
            cli_cache
        )

        return cli_session


class Paginator:  # pylint: disable=R0903
    """Boto3 generic paginator."""
    _class_logger = MODULE_LOGGER.getChild(__qualname__)

    def __init__(self, client: object, method: str):
        """Class constructor."""
        self._instance_logger = self._class_logger.getChild(str(id(self)))
        self.client = client
        self.method = method

    def paginate(self, **kwargs) -> any:
        """Paginate boto3 client methods."""
        try:
            paginator = self.client.get_paginator(self.method)

        except KeyError as e:
            self._instance_logger.error(f"Paginator method not found: {e}")
            sys.exit(-1)

        except ClientError as e:
            self._instance_logger.error(f"Fail getting paginator: {e}")
            sys.exit(-1)

        try:
            for page in paginator.paginate(**kwargs).result_key_iters():
                for result in page:
                    yield result

        except UnboundLocalError as e:
            self._instance_logger.error(f"Paginator failure: {e}")
            sys.exit(-1)

        except ClientError as e:
            self._instance_logger.error(f"Paginator failure: {e}")
            sys.exit(-1)


class BotoType:
    """Set boto3 client."""
    _class_logger = MODULE_LOGGER.getChild(__qualname__)

    def __init__(self, session: object) -> None:
        """Class constructor."""
        self._instance_logger = self._class_logger.getChild(str(id(self)))
        self.session = session

    def client(self, client: str) -> object:
        """Set boto3 client."""
        try:
            return self.session.client(client)
        except Exception as e:  # pylint: disable=W0718
            self._instance_logger.error(f"Boto3 client initialization failure: {e}")
            sys.exit(-1)

    def resource(self, resource: str) -> object:
        """Set boto3 resource."""
        try:
            return self.session.resource(resource)
        except Exception as e:  # pylint: disable=W0718
            self._instance_logger.error(f"Boto3 resource initialization failure: {e}")
            sys.exit(-1)
