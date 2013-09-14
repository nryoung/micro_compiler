"""
Data structures to be used in the micro micro compiler.
"""

from compiler_errors import OpError
from compiler_errors import LiteralError
from compiler_errors import IdError

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
            raise OpError("Operator must either be a '+' or '-'")
        else:
            self._op = o

class ExprRec(object):

    def __init__(self, expr, literal=None):
        if literal:
            self.val = expr
        else:
            self.name = expr

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, expr):
        try:
            v = int(expr)
        except ValueError:
            raise LiteralError("Invalid invalid literal with base 10: '%s'" % expr)
        else:
            self._val = v

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, expr):
        try:
            n = int(expr)
        except ValueError:
            self._name = expr
        else:
            raise IdError("Invalid Id name: '%s'" % expr)
