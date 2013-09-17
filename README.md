micro_compiler
==============

Requirements
------------
- Python version 2.7+


Test Compile:
-------------

`$ python test_compiler.py compile --in_file=<file with micro_lang> --out_file=<output file>`

- Where the `<file with micro_lang>` is the path to the file containing micro language.
- Example test files can be found in the `ext` dir.
- Where the `<output file>` is the path to the file that the compiler will output op code.
- If no output file is specified the compiler outputs by default to `output/op_code`.

Example test Compile command:
-----------------------------

`$ python test_compiler.py compile --in_file=ext/test_compile1 --out_file=output/op_code`


Test Parser:
------------

`$ python test_compiler.py parser --in_file=<file with micro_lang>`

- Where the `<file with micro_lang>` is the path to the file containing micro language.
- Example test files can be found in the `ext` dir.
- Prints out the parsed expression to stdout in BNF form.

Example test Parser command:
----------------------------

`$ python test_compiler.py parser --in_file=ext/test_parser1`


Test Scanner:
-------------

`$ python test_compiler.py scanner --in_file=<file with micro_lang>`

- Where the `<file with micro_lang>` is the path to the file containing micro language.
- Example test files can be found in the `ext` dir.
- Prints out list of scanned tokens to stdout in a list.

Example test Scanner command:
-----------------------------

`$ python test_compiler.py scanner --in_file=ext/test_scanner1`


Unit Tests:
-----------

`python test_compiler.py unit`

- Performs unit tests.
