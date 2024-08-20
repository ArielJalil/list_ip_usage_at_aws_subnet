# -*- coding: utf-8 -*-
"""Class to handle IP addresses."""

import ipaddress

from logging import getLogger
LOGGER = getLogger(__name__)


class IpAddress:
    """Handle IP addresses functions."""

    def __init__(self):
        """Class Constructor."""

    def get_ips_v4_in_cidr(self, cidr: str) -> list:
        """Get the list of IP addresses in a given CIDR."""
        return [str(ip) for ip in ipaddress.IPv4Network(cidr)]

    def get_ips_v6_in_cidr(self, cidr: str) -> list:
        """Get the list of IP addresses in a given CIDR."""
        return [str(ip) for ip in ipaddress.IPv6Network(cidr)]
