# List IP Addresses usange with an AWS subnet

Display list of IP addresses usage in a given AWS subnet

## Script usage

```bash
❯ python subnet_query.py --help
Usage: subnet_query.py [OPTIONS]

  Display the list of IP addresses in a given Subnet ID.

Options:
  -s, --subnet_id TEXT  Select Subnet ID to be queried.  [required]
  -p, --profile TEXT    Select AWS cli profile name from ~/.aws/config file
                        [default: default; required]
  -r, --region TEXT     AWS Region to run the queries.  [default: ap-
                        southeast-2]
  --help                Show this message and exit.
```

## Author and Lincense

This script has been written by [Ariel Jall](https://github.com/ArielJalil) and it is released under
 [GNU 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
