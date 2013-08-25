from scanner import Scanner
import logging
"""
Main loop to test the Scanner
"""

micro_lang1 = """BEGIN -- SOMETHING UNUSUAL
  READ(A1,New_A, D, B); 
  C:= A1 +(New_A - D) - 75; 
  New_C:=((B- (7)+(C+D)))-(3 - A1);-- STUPID FORMULA 
  WRITE(C, A1+New_C); 
  -- WHAT ABOUT := B+D;
END"""

token_list = []

if __name__ == '__main__':
    logging.basicConfig(filename='log.log', level=logging.DEBUG)

    s = Scanner(micro_lang1)

    while True:
        token = s.scan()
        logging.debug('Token: %s' % token)
        if token:
            token_list.append(token)
        if token == 'EofSym':
            break

    print token_list
