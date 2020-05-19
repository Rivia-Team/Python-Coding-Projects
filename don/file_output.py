"""
task 14 - Write a program that takes 3 command line arguments to produce a friendly
   formatted output of files greater than the specified size and older than the
   specified age:
    - directory_path -> location on the file system to analyze
    - file_size -> file size or greater in bytes that the tool should look for
    - file_age -> file age or greater in days that the tool should look for
"""
import os
import sys
import datetime


def process_args():
    """
    prints a list of files with their size for files that are greater
    than the file_size and file_age passed in as command line arguments
    :return: None
    """
    path = sys.argv[1]
    file_size = int(sys.argv[2])
    file_age = int(sys.argv[3])
    for dirpath, dirnames, files in os.walk(path):
        #for directory_name in dirnames:
         #   age_dir = datetime.date.fromtimestamp(os.stat(directory_name).st_mtime)
         #   print(age_dir)
         #   print(directory_name + " is a directory and has size: " + str(os.path.getsize(directory_name)))

        for file_name in files:
            age_file = datetime.date.fromtimestamp(os.stat(os.path.join(dirpath, file_name)).st_mtime)
            curr_date = datetime.date.today()
            delta = (curr_date - age_file).days
            if os.path.getsize(os.path.join(dirpath, file_name)) > file_size and \
                    delta > file_age:
                print(file_name + " size is: " + str(os.path.getsize(os.path.join(dirpath, file_name))) + " Bytes.")


def main():
    """
    if there is an error the user is notified that they should try again
    with valid command line arguments
    :return: None
    """
    try:
        process_args()
    except:
        print("Command line arguments must be 'path', 'size in bytes', 'age in days'")
        print("Please try again with valid command line arguments")


if __name__ == "__main__":
    main()