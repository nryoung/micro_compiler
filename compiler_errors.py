"""
Errors for the compiler
Name: Nicholas Young
Course: CSCI 4640
Assignment #1
"""

class LexicalError(Exception):
    """
    Exception raised when a lexical error is detected.
    """
    def __init__(self, bad_char):
        self.bad_char = bad_char
