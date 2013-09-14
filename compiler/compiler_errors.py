"""
Errors for the compiler
Name: Nicholas Young
Course: CSCI 4640
"""

class CompilerError(Exception):
    """
    Base class for exceptions in this compiler module.
    """
    pass

class LexicalError(CompilerError):
    """
    Exception raised when a lexical error is detected.
    """
    def __init__(self, bad_char):
        self.err = bad_char


class SyntaxError(CompilerError):
    """
    Exception raised when a syntax error is detected.
    """
    def __init__(self, syn_err):
        self.err = syn_err

class TypeError(CompilerError):
    """
    Exception raised when a type error is detected.
    """
    def __init__(self, typ_error):
        self.err = typ_error
