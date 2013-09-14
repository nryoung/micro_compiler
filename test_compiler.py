"""
Test runner for Compiler implementation.
Depending on cmd line arguments it will run specifica tests.
Name: Nicholas Young
Course: CSCI 4640
"""
import argparse
import tests
import unittest
from compiler.compiler_errors import SyntaxError, LexicalError

def test_parser(program):
    from compiler.parser import Parser

    p = Parser(program)
    try:
        while True:
            p.system_goal()
            break
    except (SyntaxError, LexicalError) as e:
        print "Lexical or Syntax error occured with char: '%s'" % e.err
    else:
        for o in p.output:
            print o

def test_scanner(program):
    from compiler.scanner import Scanner

    # Instantiate our Scanner and yield the token list
    token_list = []
    s = Scanner(program)
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

def unit_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)


if __name__ == '__main__':
    # Create cmd line object parser
    parser = argparse.ArgumentParser()
    parser.add_argument('test_type', type=str,
                        help="""The component of the compiler to be tested.
                             Options are: 'scanner' | 'parser' | 'unit'""")
    parser.add_argument('--file', type=argparse.FileType('r'),
                        help='Name of the file to be tested with.')

    args = parser.parse_args()

    # Run the specific test depending on the args passed in
    if args.test_type == 'scanner':
        test_scanner(args.file)
    elif args.test_type == 'parser':
        test_parser(args.file)
    elif args.test_type == 'unit':
        unit_tests()
    else:
        parser.print_help()
