import re
import os, time
import logging
import argparse, sys
from time import ctime 
from pathlib import Path
from os import listdir
from os.path import isfile, join
from datetime import datetime

is_printed = True
logger = None


def count_grep(pattern, file_names):
    """
    Parameters: pattern, file_names
    Brief: Counts the number of lines with the pattern in given input files
    Returns: None
    """
    global logger
    count = 0
    try:
        for name in file_names:
            f = open(name, "r")
            lines = f.readlines()
            for line in lines:
                if pattern in line and line:
                    count += 1
            logger.info("INFO: count = " + str(count))
            print(name, "count = " + str(count))
    except Exception as e:
        logger.error("ERROR: " + str(e))
        print(e)


def match_grep(pattern, file_names):
    """
    Parameters: pattern, file_names
    Brief: Prints the files having the pattern among given files
    Returns: None
    """
    try:
        file_logging = list()
        for name in file_names:
            f = open(name, "r")
            if(pattern in f.read()):
                file_logging.append(name)
                print(name)
        logger.info("INFO: Files are = " + str(file_logging))
    except Exception as e:
        logger.error("ERROR: " + str(e))
        print(e)


def line_grep(pattern, file_names):
    """
    Parameters: pattern, file_names
    Brief: Prints the line along with it's number having pattern in the given file
    Returns: None
    """
    try:
        file_logging = list()
        for name in file_names:
            print(name + ":")
            f = open(name, "r")
            lines, i, flag = f.readlines(), 1, True
            for line in lines:
                if pattern in line and line:
                    file_logging.append(str(i)+". ", line)
                    print(str(i)+". ", line)
                    flag = False
                i += 1
            if(flag):
                logger.info("INFO: No lines found matching given pattern in file " + name)
                print("No lines found matching given pattern"+"\n")
            else:
                logger.info("INFO: Lines with pattern in file " + name + " = " + str(file_logging))
    except Exception as e:
        logger.error("ERROR: " + str(e))
        print(e)


def read_grep(pattern, d_path):
    """
    Parameters: pattern, d_path
    Brief: Prints all the files with the given pattern in the current directory and sub-directories
    Returns: None
    """
    global is_printed
    files = list()
    files = [f for f in listdir(d_path) if isfile(join(d_path, f))]
    try:
        for name in files:
            f = open(join(d_path, name), "r")
            if(pattern in f.read()):
                print(name)
                if is_printed : is_printed = False 
    except Exception as e:
        logger.error("ERROR: " + str(e))
        print(e)
    subdir_path = [f.path for f in os.scandir(d_path) if f.is_dir()]
    for path in subdir_path:
        read_grep(pattern, path)
    return 


def mod_read_grep(pattern, d_path, inc_exc, flag):
    """
    Parameters: pattern, d_path, inc_exc, flag
    Brief: Modified read_prep, prints only the file name with including or excluding command.
    Returns: None
    """
    global is_printed, logger
    files = list()
    files = [f for f in listdir(d_path) if isfile(join(d_path, f))]
    try:
        for name in files:
            if(flag and inc_exc in name):
                f = open(join(d_path, name), "r")
                if(pattern in f.read()):
                    print(name)
                    if is_printed : is_printed = False 
            elif(not flag and inc_exc not in name):
                f = open(join(d_path, name), "r")
                if(pattern in f.read()):
                    print(name)
                    if is_printed : is_printed = False 
    except Exception as e:
        logger.error("ERROR: " + str(e))
        print(e)

    subdir_path = [f.path for f in os.scandir(d_path) if f.is_dir()]
    for path in subdir_path:
        mod_read_grep(pattern, path, inc_exc, flag)
    return


def read_command():
    """
    Parameters: None
    Brief: Reads and Parses the given command
    Returns: None
    """
    global is_printed, logger
    
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument('-c', action='store_true')
        parser.add_argument('-l', action='store_true')
        parser.add_argument('-n', action='store_true')
        parser.add_argument('-r', action='store_true')
        parser.add_argument("--include", action='store_const', const = "Include")
        parser.add_argument("--exclude", action='store_const', const = "Exclude")
        parser.add_argument("pattern", type=str, help="Pattern to search in a file")
        parser.add_argument("filename", nargs='+',  type=str, help="Input a valid file name or '*' for all files")
        parser.add_argument('--version', action='store_const', const="3.7.6")

        args = parser.parse_args()

        f_count = args.c
        f_match = args.l
        f_line = args.n
        f_read = args.r
        f_include = args.include
        f_exclude = args.exclude
        f_pattern = args.pattern
        f_name = args.filename
        f_version = args.version

        logger.info("INFO: Command given = " + " ".join(sys.argv))

        if(f_count):
            count_grep(f_pattern, f_name)
        elif(f_match):
            match_grep(f_pattern, f_name)
        elif(f_line):
            line_grep(f_pattern, f_name)
        elif(f_read):
            curr_directory = os.getcwd()
            if(f_include or f_exclude):
                if(f_include and f_exclude):
                    logger.error("ERROR: Can't include both include and exclude commands")
                    print("Incorrect Command: can't use both include and exclude together")
                    return
                if(f_include):
                    mod_read_grep(f_pattern, curr_directory, f_include, 1)
                if(f_exclude):
                    mod_read_grep(f_pattern, curr_directory, f_exclude, 0)
            else:
                read_grep(f_pattern, curr_directory)
            if(is_printed):
                logger.info("INFO: No files found")
                print("No files found")
        if(f_version):
                print("Version: " + f_version)
    except Exception as e:
        logger.error("ERROR: " + str(e))
        print(e)


def logger():
    """Brief Logger"""

    global logger
    logging.basicConfig(filename="grep.py.log", format='%(asctime)s %(message)s',
                        filemode='a')
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    pass


if __name__ == "__main__":
    logger()
    read_command()  