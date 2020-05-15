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
    parser = argparse.ArgumentParser(description='''Produce a friendly formatted output of files greater than the 
specified size and older than the specified age. ( Example: python3 file_lookup.py -p /home/pi -s 1 -a 1 )''')
    parser.add_argument('--directory_path', '-p', '-d', default=".", type=str,
                        help='location on the file system to analyze (default to current dir)')
    parser.add_argument('--file_size', '-s', type=int,
                        help='''file size or greater in bytes that the tool should look for.''')
    parser.add_argument('--file_age', '-a', type=int,
                        help='''file age or greater in days that the tool should look for (days).''')
    for file in lookup(parser.parse_args()):
        print(file)


def lookup(args):
    result = []
    for f in os.listdir(args.directory_path):
        pathname = os.path.join(args.directory_path, f)
        stats = os.stat(pathname)
        file_age = datetime.fromtimestamp(stats.st_mtime)
        if args.file_age is not None:
            time_boundary = datetime.now() - timedelta(days=args.file_age)
            if file_age < time_boundary:
                continue
        if args.file_size is not None:
            if stats.st_size < args.file_size:
                continue
        result.append(f"{f} - size {stats.st_size}B, mtime: {file_age}")
    return result


if __name__ == "__main__":
    main()
