# Importing Library
import argparse
import os

# Creating Parser
my_parser = argparse.ArgumentParser(prog='Program_Name', description='List the content of a directory', epilog="Enjoy the program",
                                    prefix_chars='-', allow_abbrev=True)

# Adding the arguments
my_parser.add_argument('Path', metavar='path', type=str, help='The path to list')
my_parser.add_argument('-l', '--long', action='store_true', help='enable the long list format')

# Execute parser_args()
args = my_parser.parse_args()
input_path = args.path

if not os.path.isdir(input_path):
    print('The path specified does not exist')

for line in os.listdir(input_path):
    if args.long:
        size = os.stat(os.path.join(input_path, line)).st_size
        line = '%10d %s' % (size, line)
        print(line)

