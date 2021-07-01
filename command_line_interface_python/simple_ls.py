"""This program list the folders of a give directory"""

# Importing argparse
import argparse
import os
import sys


def manual_ls():
    """This is a simple program that list the directory of a folder"""
    print("This is import: ", sys.argv)
    if len(sys.argv) > 2:
        print(" You have specified to many arguments ")
        sys.exit()
    elif len(sys.argv) < 2:
        print("You need to specify the path to be listed")
        sys.exit()

    input_path = sys.argv[1]

    if not os.path.isdir(input_path):
        print("The path provided does ot exist")
        sys.exit()
    print('\n'.join((os.listdir(input_path))))


def argparser_ls():
    my_paser = argparse.ArgumentParser(prog='Program_Name', description='List the content of a directory', epilog="Enjoy the program",
                                       prefix_chars='-')

    # Add the arguments
    my_paser.add_argument('path', metavar='path', type=str, help='The path to directory to list')

    # Executing the parser_arg() methods
    args = my_paser.parse_args()

    input_path = args.path

    if not os.path.isdir(input_path):
        print("the path specified does not exist")
        sys.exit()

    print('\n'.join(os.listdir(input_path)))


if __name__ == '__main__':
    # manual_ls()
    argparser_ls()
