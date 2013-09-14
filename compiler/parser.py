"""
Parser implementation
Name: Nicholas Young
Course: CSCI 4640
"""
from .compiler_errors import SyntaxError
from .scanner import Scanner
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
        self.build_output('<statement>')
        next_token = self.next_token()
        if next_token == 'Id':
            self.ident()
            self.match('AssignOp')
            self.expression()
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
        self.build_output('<id list>')
        self.ident()
        next_token = self.next_token()

        if next_token == 'Comma':
            self.match('Comma')
            self.id_list()
        else:
            return

    def expression_list(self):
        self.build_output('<expression list>')
        self.expression()
        next_token = self.next_token()

        if next_token == 'Comma':
            self.match('Comma')
            self.expression_list()
        else:
            return

    def expression(self):
        self.build_output('<expression>')
        self.primary()
        next_token = self.next_token()

        if next_token == 'PlusOp' or next_token == 'MinusOp':
            self.add_op()
            self.expression()
        else:
            return

    def primary(self):
        self.build_output('<primary>')
        next_token = self.next_token()

        if next_token == 'LParen':
            self.match('LParen')
            self.expression()
            self.match('RParen')

        elif next_token == 'Id':
            self.ident()

        elif next_token == 'IntLiteral':
            self.match('IntLiteral')

        else:
            raise SyntaxError(next_token)

    def ident(self):
        self.match('Id')

    def add_op(self):
        self.build_output('<add op>')
        next_token = self.next_token()

        if next_token == 'PlusOp':
            self.match('PlusOp')

        elif next_token == 'MinusOp':
            self.match('MinusOp')

        else:
            raise SyntaxError(next_token)
