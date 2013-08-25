"""
Test runner for Scanner implementation
"""
from scanner import Scanner
from scanner_errors import LexicalError
import logging

# Globals to be used in testing
micro_lang1 = """BEGIN -- SOMETHING UNUSUAL
  READ(A1,New_A, D, B); 
  C:= A1 +(New_A - D) - 75; 
  New_C:=((B- (7)+(C+D)))-(3 - A1);-- STUPID FORMULA 
  WRITE(C, A1+New_C); 
  -- WHAT ABOUT := B+D;
END"""

micro_lang2 = """BEGIN 
READ(A, B, C, D); 
E := (A + B) - (C + D); -- Calculate
WRITE(E); 
END"""

token_list = []

if __name__ == '__main__':
    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    s = Scanner(micro_lang2)

    try:
        while True:
            token = s.scan()
            logging.debug('Token: %s' % token)
            if token:
                token_list.append(token)
            if token == 'EofSym':
                break
    except LexicalError as e:
        print "Lexical Error. Unknown character: '%s'" % e.bad_char
    else:
        print token_list
