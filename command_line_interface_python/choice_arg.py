# import libraries
import argparse

# Creating parser
my_parser = argparse.ArgumentParser()

my_parser.add_argument('choice', choices=['me', 'my'], action='store')

args = my_parser.parse_args()
print(args.choice)