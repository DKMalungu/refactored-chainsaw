# Import libraries
import argparse


def abbrev_supported():
    # Creating Parser
    my_parser = argparse.ArgumentParser(prog='abbrev_example', description='Allowing or Disallowing abbreviations', epilog='Enjoy the program',
                                        prefix_chars='-')
    # Adding arguments
    my_parser.add_argument('--input', type=int, required=True)
    my_parser.add_argument('--id', type=int)

    # Executing parser
    arg = my_parser.parse_args()

    print(arg.input)


def abbrev_not_supported():
    # Create Parser
    my_parser = argparse.ArgumentParser(prog='abbrev_example', description='Allowing or Disallowing abbreviations', epilog='Enjoy the program',
                                        prefix_chars='-', allow_abbrev=False)

    # Adding arguments
    my_parser.add_argument('--input', type=int, required=True)
    my_parser.add_argument('--id', type=int)

    # Executing parser
    arg = my_parser.parse_args()

    print(arg.input)


if __name__ == '__main__':
    # abbrev_supported()
    abbrev_not_supported()
