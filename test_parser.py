"""
Test runner for Parser implementation
Name: Nicholas Young
Course: CSCI 4640
Assignment #1
"""
from parser import Parser
from compiler_errors import SyntaxError, LexicalError
import argparse

if __name__ == '__main__':
    # Add arg parsers to the program
    parser = argparse.ArgumentParser()
    parser.add_argument('program', type=argparse.FileType('r'),
                        help='Name of program to be parsed')
    args = parser.parse_args()

    # Instantiate the parser
    p = Parser(args.program)
    try:
        while True:
            p.system_goal()
            break
    except (SyntaxError, LexicalError) as e:
        print "Lexical or Syntax error occured with char: '%s'" % e.err
    else:
        for o in p.output:
            print o
