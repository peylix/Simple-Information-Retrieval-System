#!/usr/bin/env python3

import os
import sys


def get_path_of(file_name: str, ignore_existence: bool = False) -> str:
    '''
    This function is for acquiring the file path of the given file name.
    It will get the path from the command line arguments if the arguments follow the correct format.
    If the file does not exist or the arguments are not in the correct format, 
    the program will exit with an error message.
    '''
    if len(sys.argv) == 5 and sys.argv[3] == '-p':
        path = sys.argv[4]

        if os.path.exists(path):
            file_path = os.path.join(path, file_name)

            if ignore_existence:
                return file_path
            elif os.path.exists(file_path):
                return file_path
            else:
                print('Error: The file does not exist. The current recognized file path is ', file_path)
                sys.exit(1)
        else:
            print('Error: The path does not exist.')
            sys.exit(1)
    else:
        print('Error: Invalid arguments.')
        print('You can use `./query_small_corpus.py -m <mode> -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)


def get_mode(mode_list: list) -> str:
    '''
    This function gets the mode from the command line arguments.
    If the mode is not in the mode list or the arguments are not in the correct format, 
    the program will exit with an error message.
    '''
    if len(sys.argv) == 5 and sys.argv[1] == '-m':
        mode = sys.argv[2]
        if mode in mode_list:
            return mode
        else:
            print('Error: Invalid mode.')
            print('The available modes are: ', ', '.join(mode_list))
            sys.exit(1)
    else:
        print('Error: Invalid arguments.')
        print('You can use `./query_small_corpus.py -m <mode> -p /path/to/comp3009j-corpus-small` to run the program.')
        sys.exit(1)


if __name__ == '__main__':
    mode_list = ['interactive', 'automatic']
    mode = get_mode(mode_list)
    path = get_path_of('documents')