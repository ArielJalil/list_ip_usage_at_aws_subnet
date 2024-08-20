# -*- coding: utf-8 -*-
"""Display list of IP addresses usage in a given subnet."""

# https://github.com/jagadishrajr/findfreeipinawssubnet

import click

from classes.common import Color
from classes.python_arrays import ListToColumns, GetItemFrom
from classes.python_sdk import AwsSession
from classes.subnet import AwsSubnet

from logging import getLogger

DEFAULT_CLI_PROFILE = 'default'
DEFAULT_REGION = 'ap-southeast-2'
LOGGER = getLogger(__name__)


@click.command()
@click.option(
    '-s',
    '--subnet_id',
    required=True,
    nargs=1,
    help='Select Subnet ID to be queried.'
)
@click.option(
    '-p',
    '--profile',
    required=True,
    default=DEFAULT_CLI_PROFILE,
    show_default=True,
    nargs=1,
    help='Select AWS cli profile name from ~/.aws/config file'
)
@click.option(
    '-r',
    '--region',
    default=DEFAULT_REGION,
    show_default=True,
    nargs=1,
    help='AWS Region to run the queries.'
)
def subnet_query(subnet_id: str, profile: str, region: str) -> None:
    """Display the list of IP addresses in a given Subnet ID."""

    # SDK authorization
    session = AwsSession(profile, region).cli()

    # Get subnet details
    subnet = AwsSubnet(session, subnet_id)
    subnet_name = GetItemFrom(subnet.tags).by_tag_key('Name')

    # Make up an array of IP addresses to be displayed:
    pick = Color()
    ip_count = 0
    ip_taken_count = 0
    ip_free = 0
    ips_to_display = []

    for ip in subnet.ips_in_cidr():
        if ip['Usage'] == 'Free':
            color = pick.green
            ip_free += 1
        else:
            ip_taken_count += 1
            color = pick.red

        ips_to_display.append(f"{color}{ip_count:3d} | {ip['IpAddress']:15s} | {ip['Usage']:25s}")
        ip_count += 1

    # Display the list of IPs in the given subnet
    col_width = len(ips_to_display[0]) - 3  # Removing 3 characters from the items added by color setting
    ListToColumns(ips_to_display, col_width).display()

    # Summary
    print(f"{pick.no_color}\nSummary:\n")
    print(f"Subnet id....................: {subnet_id}")

    if subnet_name:
        print(f"Subnet name..................: {subnet_name}")

    print(f"Subnet CIDR..................: {subnet.cidr}")
    print(f"IPs in this Subnet...........: {ip_count}")
    print(f"IPs available in this Subnet.: {ip_count - 5}")
    print(f"IPs free.....................: {ip_free}")
    print(f"IP/s in use..................: {ip_taken_count - 5}")


if __name__ == '__main__':
    subnet_query()
