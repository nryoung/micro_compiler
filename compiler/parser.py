"""
Parser implementation
"""
from .compiler_errors import SyntaxError
from .scanner import Scanner
from .data_structures import ExprRec, OpRec
import sem_routines

class Parser(object):

    def __init__(self, micro_lang):
        self.scanner = Scanner(micro_lang)
        self.terminals = []
        self.output = []
        self.symbol_table = []

    def build_output(self, s):
        if self.terminals:
            temp = ' '.join(self.terminals)
            temp += ' %s' % s
            self.output.append(temp)
        else:
            self.output.append(s)

    def next_token(self):
        temp_micro = self.scanner.micro_lang
        next_token = self.scanner.scan()
        self.scanner.micro_lang = temp_micro
        return next_token

    def match(self, legal_token):
        current_token = self.scanner.scan()

        if current_token != legal_token:
            raise SyntaxError(current_token)
        else:
            self.terminals.append(current_token)

    def system_goal(self):
        self.build_output('<system goal>')
        self.program()
        self.match('EofSym')
        self.build_output('')
        sem_routines.finish()


    def program(self):
        self.build_output('<program>')
        sem_routines.start(self.symbol_table)
        self.match('BeginSym')
        self.statement_list()
        self.match('EndSym')
        self.build_output('')

    def statement_list(self):
        self.build_output('<statement list>')
        self.statement()
        next_token = self.next_token()
        if next_token == 'Id':
            self.statement_list()
        elif next_token == 'ReadSym':
            self.statement_list()
        elif next_token == 'WriteSym':
            self.statement_list()
        else:
            return

    def statement(self):
        identifier = ExprRec()
        expr = ExprRec()
        self.build_output('<statement>')
        next_token = self.next_token()
        if next_token == 'Id':
            self.ident(identifier)
            self.match('AssignOp')
            self.expression(expr)
            sem_routines.assign(identifier, expr)
            self.match('SemiColon')

        elif next_token == 'ReadSym':
            self.match('ReadSym')
            self.match('LParen')
            self.id_list()
            self.match('RParen')
            self.match('SemiColon')

        elif next_token == 'WriteSym':
            self.match('WriteSym')
            self.match('LParen')
            self.expression_list()
            self.match('RParen')
            self.match('SemiColon')

        else:
            raise SyntaxError(next_token)

    def id_list(self):
        identifier = ExprRec()
        self.build_output('<id list>')
        self.ident(identifier)
        sem_routines.read_id(identifier)
        next_token = self.next_token()

        if next_token == 'Comma':
            self.match('Comma')
            self.id_list()
        else:
            return

    def expression_list(self):
        expr = ExprRec()
        self.build_output('<expression list>')
        self.expression(expr)
        sem_routines.write_expr(expr)
        next_token = self.next_token()

        if next_token == 'Comma':
            self.match('Comma')
            self.expression_list()
        else:
            return

    def expression(self, result):
        left_oper = ExprRec()
        right_oper = ExprRec()
        op = OpRec()
        self.build_output('<expression>')
        self.primary(left_oper)
        next_token = self.next_token()

        if next_token == 'PlusOp' or next_token == 'MinusOp':
            self.add_op(op)
            self.expression(right_oper)
            temp = sem_routines.get_infix(left_oper, op, right_oper, self.symbol_table)

            # Note we have to explicitly set attribute values here instead of a straight
            # assignment like: result = sem_routines(...).
            # Python rebinds the name result to the temp obj. instead of updating the
            # current one. This causes problems when the temp obj. is GC'ed.
            if temp.name:
                result.name = temp.name
            elif temp.val:
                result.val = temp.val
        else:
            # See comment above as to why attributes are set explicitly
            if left_oper.name:
                result.name = left_oper.name
            elif left_oper.val:
                result.val = left_oper.val
            return

    def primary(self, result):
        self.build_output('<primary>')
        next_token = self.next_token()

        if next_token == 'LParen':
            self.match('LParen')
            self.expression(result)
            self.match('RParen')

        elif next_token == 'Id':
            self.ident(result)

        elif next_token == 'IntLiteral':
            self.match('IntLiteral')
            sem_routines.proc_literal(result, self.scanner.buffer)

        else:
            raise SyntaxError(next_token)

    def ident(self, result):
        self.match('Id')
        sem_routines.process_id(result, self.scanner.buffer, self.symbol_table)

    def add_op(self, op):
        self.build_output('<add op>')
        next_token = self.next_token()

        if next_token == 'PlusOp':
            self.match('PlusOp')
            sem_routines.process_op(op, '+')

        elif next_token == 'MinusOp':
            self.match('MinusOp')
            sem_routines.process_op(op, '-')

        else:
            raise SyntaxError(next_token)

    def check_input(self, valid_set, follow_set, header_set):
        next_token = self.next_token()

        if next_token in valid_set:
            return
        else:
            illegal_token = next_token

            while next_token not in valid_set and next_token not in follow_set and next_token not in header_set:
                next_token = self.next_token()

            raise SyntaxError(illegal_token)
