"""
TASK 16

 task 16 - Write a program that plays the game BlackJack with a user. For this
    exercise you can use procedural or OOP programming styles. Research the rules
    of BlackJack to ensure your game is authentic.

Completed: AP -

Write a program that takes 3 command line arguments to produce a friendly

formatted output of files greater than the specified size and older than the

specified age:

- directory_path -> location on the file system to analyze

- file_size -> file size or greater in bytes that the tool should look for

- file_age -> file age or greater in days that the tool should look for
    import sys
"""
import datetime
import os
import sys


def validate_arguments(argvs: list, validationamt=4) -> bool:
    """Validate we have all the required options."""
    if len(argvs) == validationamt:
        if os.path.isdir(sys.argv[1]):
            try:
                int(sys.argv[2])
                int(sys.argv[3])
            except ValueError as e:
                print(f"Not a valid input for days. ERROR: {e}")
                return False
        elif not os.path.isdir(sys.argv[1]):
            print("ERROR: Invalid directory.")
            return False
        return True
    else:
        return False


def display_hints():
    """Remind user of correct inputs to this application."""
    print('''\n
    First argument: directory path "/etc/services" \n
    Second argument: file size or greater in bytes "1000" \n
    Third argument: file age or greater in days to look for "7" \n''')


def analyze_directory_py(mydir: str, minsize: str, mindate: str) -> list:
    """ Parse the arguments. """
    startdate = datetime.date.today() - datetime.timedelta(days=int(mindate))
    print("  - Looking for files older than: {}".format(startdate))
    print("  - Looking for files greater than: {} bytes \n".format(minsize))
    try:
        filesindir = os.listdir(mydir)
    except FileNotFoundError as e:
        print(f"The directory has changed since program start up. {e}")
    validfileslist = []
    for file in filesindir:
        if os.path.getsize(file) > int(minsize):
            timestamp = datetime.date.fromtimestamp(os.path.getmtime(file))
        if timestamp < startdate:
            validfileslist.append([file, timestamp.__str__(), os.path.getsize(file)])
    return validfileslist


def main():
    if validate_arguments(sys.argv):
        print("-*- Valid inputs. Processing your request! -*-")
        myvalidfiles = analyze_directory_py(sys.argv[1], sys.argv[2], sys.argv[3])
        print("****** Files Older Than {} Days and Larger than {} Bytes. ******".format(sys.argv[3], sys.argv[2]))
        print(" - Source Directory: {}".format(sys.argv[1]))
        for file in myvalidfiles:
            try:
                print("File {} was last modified on {} and is {} bytes large.".format(file[0], file[1], file[2]))
            except IndexError as e:
                print(f" File info not properly returned.  {e}")
    else:
        display_hints()


if __name__ == "__main__":
    main()



