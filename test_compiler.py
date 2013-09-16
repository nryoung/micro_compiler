"""
Test runner for Compiler implementation.
Depending on cmd line arguments it will run specific tests.
Name: Nicholas Young
Course: CSCI 4640
"""
import argparse
import tests
import unittest
import traceback
import sys
from compiler.compiler_errors import SyntaxError, LexicalError

# Small class that collects all sys_stdout which
# allows it to be later written to a file.
class WriteObj(object):
    def __init__(self):
        self.content =""
    def write(self, s):
        self.content += s

def test_compile(in_file, out_file):
    from compiler.parser import Parser
    p = Parser(in_file)
    try:
        output = WriteObj()
        sys.stdout = output
        p.system_goal()
    except Exception as e:
        print traceback.format_exc()
    else:
        sys.stdout = sys.__stdout__
        out_file.write(output.content)
        print "Compiled to location: %s" % out_file.name

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
                             Options are: 'scanner' | 'parser' | 'unit' | 'compile'""")
    parser.add_argument('--in_file', type=argparse.FileType('r'),
                        help='Name of the input file.')

    parser.add_argument('--out_file', default='output/op_code',
                        type=argparse.FileType('w'),
                        help='Name of the output file.')

    args = parser.parse_args()

    # Run the specific test depending on the args passed in
    if args.test_type == 'scanner':
        test_scanner(args.in_file)
    elif args.test_type == 'parser':
        test_parser(args.in_file)
    elif args.test_type == 'unit':
        unit_tests()
    elif args.test_type == 'compile':
        test_compile(args.in_file, args.out_file)
    else:
        parser.print_help()
