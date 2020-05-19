# 8. task 14 - Write a program that takes 3 command line arguments to produce a friendly
#    formatted output of files greater than the specified size and older than the
#    specified age:
#     - directory_path -> location on the file system to analyze
#     - file_size -> file size or greater in bytes that the tool should look for
#     - file_age -> file age or greater in days that the tool should look for

import argparse
import os
from datetime import datetime, timedelta


def main():
    """ Parse arguments and execute search """

    parser = argparse.ArgumentParser(description='''Produce a friendly formatted output of files greater than the 
specified size and older than the specified age. ( Example: python3 file_lookup.py -p /home/pi -s 1 -a 1 )''')
    parser.add_argument('--directory_path', '-p', '-d', default=".", type=str,  # Default to current directory
                        help='location on the file system to analyze (default to current dir)')
    parser.add_argument('--file_size', '-s', type=positive_integer,
                        help='''file size or greater in bytes that the tool should look for (bytes).''')
    parser.add_argument('--file_age', '-a', type=positive_integer,
                        help='''file age or greater in days that the tool should look for (days).''')
    for file in lookup(parser.parse_args()):
        print(file)


def positive_integer(param):
    try:
        value = int(param)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Argument '{param}' needs to be a positive integer.")
    if value < 0:
        raise argparse.ArgumentTypeError(f"Argument '{param}' needs to be a positive integer.")
    return value


def lookup(args):
    """ Returns a list of files matching the parameters"""

    result = []
    try:
        for f in os.listdir(args.directory_path):  # Iterate over directory
            pathname = os.path.join(args.directory_path, f)
            stats = os.stat(pathname)
            if os.path.isdir(pathname):  # exclude directories
                continue
            file_age = datetime.fromtimestamp(stats.st_mtime)
            if args.file_age is not None:  # exclude files newer than param
                time_boundary = datetime.now() - timedelta(days=args.file_age)
                if file_age > time_boundary:
                    continue
            if args.file_size is not None:  # exclude files smaller than param
                if stats.st_size < args.file_size:
                    continue
            result.append(f"{f} - size {stats.st_size}B, mtime: {file_age}")
    except FileNotFoundError:
        print("Please enter a valid directory.")
    except PermissionError:
        print("You do not have sufficient permissions to this directory.")
    return result


if __name__ == "__main__":
    main()
