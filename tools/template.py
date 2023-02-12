#!/usr/bin/env python3

description = '''
<INSERT TOOL DESCRIPTION HERE>
'''

example = f"{__file__} -a -b -c"

#######################
### Argument Parser ***
#######################
from argparse import ArgumentParser, RawTextHelpFormatter
import sys

parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description=description, epilog=example) # Change formatter class for different help styles
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')
required.add_argument("-a", "--a_name", type=str, default='-', required=True,
                    help="<ARGUMENT DESCRIPTION HERE>")
optional.add_argument("-b", "--b_name", type=int, default=20,
                    help="<ARGUMENT DESCRIPTION HERE>")
optional.add_argument("-c", "--c_name", action='store_true', default=False,
                    help="<ARGUMENT DESCRIPTION HERE>")
optional.add_argument("-v", "--verbose", action="store_true", default=False,
                    help="Print out additional information from the tool.")
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()
a_name = args.a_name
b_name = args.b_name
c_name = args.c_name
verbose = args.verbose

##############################
### Libraries and Packages ***
##############################
import os, contextlib, subprocess
import gzip, bz2, zipfile

MAGIC_DICT = {
    b"\x1f\x8b\x08": "gz",
    b"\x42\x5a\x68": "bz2",
    b"\x50\x4b\x03\x04": "zip"
    } # used for determining file compression

MAX_LEN = max(len(x) for x in MAGIC_DICT)

###########################
### Essential Functions ***
###########################
def verboseprint(*args, **kwargs):
    '''Function for printing when verbose option selected.'''
    print(*args, **kwargs) if verbose else lambda *a, **k: None

def file_type(filename):
    '''Detects filetype by magic values. Used in smart_open function to open files.'''
    with open(filename, 'rb') as f:
        file_start = f.read(MAX_LEN)
    for magic, filetype in MAGIC_DICT.items():
        if file_start.startswith(magic):
            return filetype
    return "no match"

@contextlib.contextmanager
def smart_open(filename, mode='Ur'):
    '''Determine if file is standard input or provided in argument. If argument, determine compression then open accordingly.'''
    if filename == '-' or filename == "" or filename == None:
        fh = sys.stdin
    else:
        ft = file_type(filename)
        if ft == "gz":
            fh = gzip.open(filename, 'rb')
        elif ft == "bz2":
            fh = bz2.open(filename, 'rb')
        elif ft == "zip":
            fh = zipfile.open(filename, 'rb')
        else:
            try:
                fh = open(filename, 'rb')
            except OSError:
                print("Error: Could not open/read inputFile.")
                sys.exit()
    try:
        yield fh
    finally:
        if filename != '-':
            fh.close()

############
### Main ***
############
def main():
    pass
    
########################
### Boilerplate Code ***
########################
if __name__ == "__main__":
    main()
