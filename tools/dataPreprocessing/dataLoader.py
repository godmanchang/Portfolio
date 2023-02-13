#!/usr/bin/env python3

# This submodule contains the fileOpener class, which automatically determines file compression to open the file

##############################
### Libraries and Packages ***
##############################
import contextlib

###############
### Classes ***
###############
class fileOpener:
    def __init__(self, filename: str):
        self.filename = filename
        self.filetype = self.__determineFileType__()
    
    def __determineFileType__(self):
        '''Detects filetype by magic values. Used in smart_open function to open files.'''
        _MAGIC_DICT = {
            b"\x1f\x8b\x08": "gz",
            b"\x42\x5a\x68": "bz2",
            b"\x50\x4b\x03\x04": "zip"
        } # used for determining file compression

        _MAX_LEN = max(len(x) for x in _MAGIC_DICT)

        with open(self.filename, 'rb') as f:
            file_start = f.read(_MAX_LEN)
        for magic, filetype in _MAGIC_DICT.items():
            if file_start.startswith(magic):
                return filetype
        return "no match"

    @contextlib.contextmanager
    def open(self, mode='Ur'):
        '''Determine if file is standard input or provided in argument. If argument, determine compression then open accordingly.'''
        ft = self.filetype
        if ft == "gz":
            import gzip
            fh = gzip.open(self.filename, 'rb')
        elif ft == "bz2":
            import bz2
            fh = bz2.open(self.filename, 'rb')
        elif ft == "zip":
            import zipfile
            fh = zipfile.open(self.filename, 'rb')
        else:
            try:
                fh = open(self.filename, 'rb')
            except OSError:
                print("Error: Could not open/read inputFile.")
                sys.exit()
        try:
            yield fh
        finally:
            if self.filename != '-':
                fh.close()

    def toPandas(self, header=0, sep=","):
        '''Converts read input to pandas dataframe. Default delimiter = ',' and assumes header'''
        import pandas
        ft = self.filetype
        if ft == "gz":
            compression = "gzip"
        elif ft == "bz2":
            compression = "bz2"
        elif ft == "zip":
            compression = "zip"
        else:
            compression = "infer"
        df = pandas.read_csv(self.filename, compression=compression, header=header, sep=sep)
        return df

    def __repr__(self):
        return f"File Opener: {self.filename} with file type {self.filetype} detected."