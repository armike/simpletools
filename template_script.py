#!/usr/bin/python
"""
Sample call:

  my_script.py --required_arg user_signup --properties user_id phone email
"""
import sys, argparse


def main(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--required_arg', help='A required arg',
                        required=True)
    parser.add_argument('--properties', nargs='+',
                        help='At least one property is required',
                        required=True)
    args = parser.parse_args(args)
    # args are access like args.required_arg


if __name__ == '__main__':
    main(sys.argv[1:])
