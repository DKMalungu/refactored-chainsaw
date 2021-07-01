# Importing Libraries
import argparse

# Create Parser
my_paser = argparse.ArgumentParser(fromfile_prefix_chars='@', prog='loading_arguments_file', description="The program loads argument from file",
                                   epilog='Enjoy the program', prefix_chars='-')
my_paser.add_argument('a', help='a First Argument')
my_paser.add_argument('b', help='a Second Argument')
my_paser.add_argument('c', help='a Third Argument')
my_paser.add_argument('d', help='a Fourth Argument')
my_paser.add_argument('e', help='a Fifth Argument')
my_paser.add_argument('-v', '--verbose', action='store_true', help='an optional argument')

# Executing parser
my_paser.parse_args()

print("If your reading this line it means that you have provided all the parameters")


