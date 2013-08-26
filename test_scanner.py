"""
Test runner for Scanner implementation
Name: Nicholas Young
Course: CSCI 4640
Assignment #1
"""
from scanner import Scanner
from scanner_errors import LexicalError
import argparse


token_list = []

if __name__ == '__main__':

    # Add argument parsers to the program
    parser = argparse.ArgumentParser()
    parser.add_argument('program', type=argparse.FileType('r'),
                        help='Name of program to be scanned')
    args = parser.parse_args()

    # Instantiate our Scanner and yield the token list
    s = Scanner(args.program)
    try:
        while True:
            token = s.scan()
            if token:
                token_list.append(token)
            if token == 'EofSym':
                break
    except LexicalError as e:
        print "Lexical Error. Unknown character: '%s'" % e.bad_char
    else:
        print token_list
