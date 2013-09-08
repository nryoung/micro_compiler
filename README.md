Name: Nicholas Young  
Course: CSCI 4640

Requirements
============
- Python version 2.7.3+

Test Parser:
============

`$ python test_compiler.py parser --file=<file with micro_lang>`

- Where the `<file with micro_lang>` is the path to the file containing micro language.
- Example test files can be found in the `ext` dir.
- Prints out the parsed expression to stdout in BNF form.

Example test Parser command:
----------------------------

`$ python test_compiler.py parser --file=ext/test_parser1`


Test Scanner:
=============

`$ python test_compiler.py scanner --file=<file with micro_lang>`

- Where the `<file with micro_lang>` is the path to the file containing micro language.
- Example test files can be found in the `ext` dir.
- Prints out list of scanned tokens to stdout in a list.

Example test Scanner command:
-----------------------------

`$ python test_compiler.py scanner --file=ext/test_scanner1`


Unit Tests:
===========

- Coming to compiler near you soon!
