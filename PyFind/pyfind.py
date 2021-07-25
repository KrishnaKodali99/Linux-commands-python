import re
import os, time
import logging
import argparse, sys
from time import ctime 
from pathlib import Path
from os import listdir
from os.path import isfile, join
from datetime import datetime

months = [0, "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
logger = None

def abort():
    """
    Parameters: None
    Brief: Prints only if no files are found
    Returns: None
    """
    print("No files found")


def execute_command(f_path, f_type, f_atime, f_gname, f_name, f_regex, f_newer):
    """
    Parameters: f_path, f_type, f_atime
                f_gname, f_name, f_regex, f_newer
    Brief: Executes the given command
    Returns: None
    """
    files = list()
    if(f_path.exists()):
        if f_path.is_dir():
            files = [f for f in listdir(f_path) if isfile(join(f_path, f))]

            if(f_type):
                files = [f for f in files if(f.endswith (f_type))]
                if(len(files) == 0):
                    abort()
                    return

            if(f_atime):
                t_files = list()
                for f in files:
                    t = time.ctime(os.stat(join(f_path, f)).st_atime).split()             
                    a_t = t[3].split(":")
                    access_time = datetime(int(t[4]), months.index(t[1][0:3].lower()), int(t[2]), int(a_t[0]), int(a_t[1]), int(a_t[2]))
                    diff = str(datetime.now() - access_time)
                    if "day" in diff:    
                        diff = diff.split()
                        if(int(diff[0]) < int(f_atime)):
                            t_files.append(f)
                files = t_files[:]
                if(len(files) == 0):
                    abort()
                    return

            if(f_name):
                files = [f for f in files if(f.split(".")[0] == f_name)]
                if(len(files) == 0):
                    abort()
                    return

            if(f_gname):
                f_path.group()
                pass

            if(f_regex):
                files = [f for f in files if(len(re.findall(f_regex, f)) > 0)]
                if(len(files) == 0):
                    abort()
                    return

            if(f_newer == "file"):
                t_files = list()
                for f in files:
                    t = time.ctime(os.stat(join(f_path, f)).st_atime).split()               
                    a_t = t[3].split(":")
                    access_time = datetime(int(t[4]), months.index(t[1][0:3].lower()), int(t[2]), int(a_t[0]), int(a_t[1]), int(a_t[2]))
                    diff = str(datetime.now() - access_time)
                    if "0:00:00" in diff:    
                        t_files.append(f)
                files = t_files[:]
                if(len(files) == 0):
                    abort()
                    return

            if(len(files) == 0):
                logger.info("INFO: No files found")
                print("No files found on given constraints")
            else:
                logger.info("INFO: Files found for given command = " + str(files))
                for f in files:
                    print(f)

    else:
        logger.error("ERROR: Command Failed, enter valid path")
        print("Path doesn't exist")


def read_command():
    """
    Parameters: None
    Brief: Reads and Parses the given command
    Returns: None
    """
    global logger
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument("-path", "--path", type=Path, help = "Give a valid path")
        parser.add_argument("-type", "--type", help = "Type of file")
        parser.add_argument("-atime", "--atime", help = "Access time of file")
        parser.add_argument("-gname", "--gname", help = "Group name of file")
        parser.add_argument("-name", "--name", help = "Base of a file name")
        parser.add_argument("-regex", "--regex", help = "Give Regex Pattern to find file")
        parser.add_argument("-newer", "--newer", help = "Find newly created files")
        parser.add_argument('--version', action='store_const', const="3.7.6")
        args = parser.parse_args()

        f_path = args.path
        f_type = args.type
        f_atime = args.atime 
        f_gname = args.gname
        f_name = args.name
        f_regex = args.regex
        f_newer = args.newer
        f_version = args.version

        logger.info("INFO: Command given = " + " ".join(sys.argv))
        if(f_path):
            execute_command(f_path, f_type, f_atime, f_gname, f_name, f_regex, f_newer)
            if(f_version):
                print("Version: " + f_version)
        else:
            logger.error("ERROR: Incorrect Command, enter any path")
            print("Enter any path")

    except Exception as e:
        logger.error("ERROR: " + e)
        print(e)


def logger():
    """Brief Logger"""

    global logger
    logging.basicConfig(filename="find.py.log", format='%(asctime)s %(message)s',
                        filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    pass


if __name__ == "__main__":
    logger()
    read_command()