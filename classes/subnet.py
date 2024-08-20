# -*- coding: utf-8 -*-
"""Class to handle subnets with AWS SDK for Python - Boto3."""

from botocore.exceptions import ClientError, UnauthorizedSSOTokenError

from classes.ip_addresses import IpAddress
from classes.python_arrays import GetItemFrom
from classes.python_sdk import BotoType, Paginator

from logging import getLogger
MODULE_LOGGER = getLogger(__name__)

class AwsSubnet:
    """Handle AWS a subnet boto3 ec2 resource."""

    def __init__(self, session: object, subnet_id) -> None:
        """Class constructor."""
        self.session = session
        self.subnet_id = subnet_id
        self.resource = BotoType(session).resource('ec2')
        self.subnet = self.resource.Subnet(subnet_id)
        self.cidr = self.subnet.cidr_block
        self.tags = self.subnet.tags

    def ips_in_cidr(self) -> any:
        """Create an array with all IPs in the CIDR and display usage."""

        # Get the list of IP addresses in a given CIDR block
        all_ips_in_cidr_block = IpAddress().get_ips_in_cidr(self.cidr)
        ips_in_block = len(all_ips_in_cidr_block)

        # Get the list of used ENIs in a given Subnet ID
        filters = [
            {
                'Name': 'subnet-id',
                'Values': [
                    self.subnet_id,
                ]
            }
        ]
        client = BotoType(self.session).client('ec2')
        network_interfaces = list(
            Paginator(client, 'describe_network_interfaces').paginate(Filters=filters)
        )

        # Create a full list of IPs in the subnet with usage details
        ip_count = 0
        for ip in all_ips_in_cidr_block:
            if ip_count == 0:
                detail = "Network"
            elif ip_count == 1:
                detail = "Reserved: Router"
            elif ip_count == 2:
                detail = "Reserved: DNS"
            elif ip_count == 3:
                detail = "Reserved: future use"
            elif ip_count == ips_in_block - 1:
                detail = "Broadcast: Blocked"
            else:
                eni = GetItemFrom(network_interfaces).by_key_pair('PrivateIpAddress', ip)
                if eni:
                    detail = f"{eni['Status']}: {eni['InterfaceType']}"
                else:
                    detail = "Free"

            ip_count += 1

            yield {
                'IpAddress': ip,
                'Usage': detail
            }


class AwsSubnets:
    """Handle AWS subnets boto3 ec2 client."""
    _class_logger = MODULE_LOGGER.getChild(__qualname__)

    def __init__(self, session: object) -> None:
        """Class constructor."""
        self._instance_logger = self._class_logger.getChild(str(id(self)))
        self.ec2 = BotoType(session).client('ec2')

    def describe(self, subnet_ids: list) -> dict:
        """Get details of a given list of Subnet IDs."""
        try:
            subnets = self.ec2.describe_subnets(
                SubnetIds=subnet_ids,
            )
            return subnets['Subnets']

        except ClientError as e:
            self._instance_logger.error(e)

        except UnauthorizedSSOTokenError as e:
            self._instance_logger.error(e)