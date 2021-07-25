# Linux Commands in Python

## PyGrep

To run pygrep:
```
python pygrep.py [options] PATTERN [FILE_NAME]
```
* --help: Output a brief help message.

* -c, --count: Suppress normal output; instead print a count of matching lines for each input file. 

* -l, --files-with-matches: Suppress normal output; instead print the name of each input file from which 
output would normally have been printed. The scanning will stop on the first match.

* -n, --line-number: Prefix each line of output with the line number within its input file.

* -R, -r, --recursive: Read all files under each directory, recursively; this is equivalent to the -d recurse
option.

* --include=PATTERN: Recurse in directories only searching file matching PATTERN.

* --exclude=PATTERN: Recurse in directories skip file matching PATTERN.

* -V, --version: Print the version number of grep to standard error.

* --benchmark: Run benchmark on core functions

All the logs will be logged in grep.py.log

## PyFind
To run pyfind:

```
python pyfind.py [path...] [expression]
```
* --help: Output a brief help message. 

* -type type: File is of type ‘type’.

* -atime n: File was last accessed n*24 hours ago.

* -group gname: File belongs to group gname (numeric group ID allowed). 

* -name pattern: Base of file name (the path with the leading directories removed) matches shell pattern pattern.

* -regex pattern: File name matches regular expression pattern. This is a match on the whole path, not a search.

* -newer file : File was modified more recently than file.

* -V, --version: Print the version number of find to standard error.

* --benchmark: Run benchmark on core functions