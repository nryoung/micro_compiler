"""
Auxiliary Routines for the micro compiler.
"""

# Globals
max_temp = 0
output_file = "compiled_code/op_code"

def generate(s1, s2, s3, s4=None, output_file=output_file):
    with open(output_file, 'a') as f:
        if s4:
            f.write("%s %s, %s, %s\n" % (s1, s2, s3, s4))
        else:
            f.write("%s %s, %s\n" % (s1, s2, s3))


def extract(e):
    try:
        return str(e.name)
    except AttributeError:
        return int(e.val)

def extract_op(o):
    if o.op == "+":
        return "ADD"
    else:
        return "SUB"

def look_up(s, symbol_table):
    if s in symbol_table:
        return  True
    else:
        return False

def enter(s, symbol_table):
    symbol_table.append(s)

def check_id(s, symbol_table):
    if not look_up(s, symbol_table):
        enter(s, symbol_table)
        generate("DECLARE", s, "Integer")

def get_temp(symbol_table):
    global max_temp
    max_temp += 1

    temp_name = "Temp&%s" % max_temp
    check_id(temp_name, symbol_table)
    return temp_name
