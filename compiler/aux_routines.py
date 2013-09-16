"""
Auxiliary Routines for the micro compiler.
Name: Nicholas Young
Course: CSCI 4640
"""
import sys

# Globals
max_temp = 0

def generate(s1, s2=None, s3=None, s4=None):
    if s4:
        sys.stdout.write("%s %s, %s, %s\n" % (s1, s2, s3, s4))
    elif s3:
        sys.stdout.write("%s %s, %s\n" % (s1, s2, s3))
    else:
        sys.stdout.write("%s" % s1)

def extract(e):
    if e.name:
        return str(e.name)
    else:
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
