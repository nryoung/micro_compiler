"""
Data structures to be used in the micro micro compiler.
"""

from compiler_errors import TypeError

class OpRec(object):

    allowed_vals = ['-', '+']

    def __init__(self, operator):
        self.op = operator

    @property
    def op(self):
        return self._op

    @op.setter
    def op(self, o):
        if o not in self.allowed_vals:
            raise TypeError("Operator must either be a '+' or '-'")
        else:
            self._op = o
