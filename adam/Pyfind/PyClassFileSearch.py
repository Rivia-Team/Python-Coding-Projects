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
import subprocess
import os
import sys


def validate_arguments(argvs: int, validationamt=4) -> bool:
    """Validate we have all the required options."""
    if len(argvs) == validationamt:
        print(os.path.isdir(sys.argv[1]))
        if os.path.isfile(sys.argv[1]) == True:
            int(sys.argv[2])
            try:
                print(int(sys.argv[2]))
            except ValueError as e:
                print(f"Not a valid input for size. ERROR: {e}")
                return False
            try:
                int(sys.argv[3])
            except ValueError as e:
                print(f"Not a valid input for days. ERROR: {e}")
                return False
        elif os.path.isdir(sys.argv[1]) == False:
            print("ERROR: Invalid directory.")
            return False
        return True
    else:
        return False


def display_hints():
    """Remind user correct inputs to this application."""
    print('''\n
    First argument: directory path "/etc/services" \n
    Second argument: file size or greater in bytes "1000" \n
    Third argument: file age or greater in days to look for "7" \n''')


def analyze_directory(mydir: str, minsize: str, mindate: str) -> bytes:
    """ Output the directory and organize.ArithmeticError """
    try:
        myout = subprocess.run(["find","{}".format(mydir),"-mtime","+"+mindate,"-size","+"+minsize+"c","-ls"],capture_output=True)
        return myout.stdout
    except FileNotFoundError as e:
        print(f"There was an issue with the command syntax. ERROR: {e}")
    except TypeError as e:
        print(f"Use python 3.7+ ERROR: {e}")

def analyze_directory_py(mydir: str, minsize: str, mindate: str):
    startdate = datetime.date.today() - datetime.timedelta(days=int(mindate))
    print("Looking for files older than: {}".format(startdate))
    filesindir = os.listdir(mydir)
    validfileslist = []
    for file in filesindir:
        if os.path.getsize(file) > int(minsize):
            print("FILE {} is GREATER than desired size!".format(file))
            timestamp = datetime.date.fromtimestamp(os.path.getmtime(file))
            if (timestamp > startdate):
                print("Comparing {} to {}".format(timestamp, startdate))
                print("This file: {} has a modified date of {}:".format(file, timestamp))
                validfileslist.append(file)
        else:
            print("FILE {} is LESS than desired size!".format(file))
    return validfileslist

def main():
    if validate_arguments(sys.argv) == True:
        print("Valid inputs. Processing your request!")
        #mydir = analyze_directory(sys.argv[1],sys.argv[2],sys.argv[3])
        mynewdir = analyze_directory_py(sys.argv[1], sys.argv[2], sys.argv[3])
        print(mynewdir)
    else:
        display_hints()


if __name__ == "__main__":
    main()



