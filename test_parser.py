"""
Test runner for Parser implementation
Name: Nicholas Young
Course: CSCI 4640
Assignment #1
"""
from parser import Parser
from compiler_errors import SyntaxError
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
    except SyntaxError as e:
        print "Syntax Error: '%s'" % e.syn_err
    else:
        for o in p.output:
            print o
