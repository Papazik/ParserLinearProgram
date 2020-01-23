# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from parse import parse
from collections import deque
import numpy as np

def find_symbol(line):
    for l in line:
        if l == '=':
            return 0 
        elif l == '<':
            return -1
        elif l == '>':
            return 1

def get_vars(var_line):
    v = var_line.split('+')
    values = []
    for var in v:
        var2 = var.strip()
        d = deque()
        for c in var2:
            if c.lower() == 'x':
                break
            d.append(c)
        if (len(list(d)) > 0):
            values.append(float(''.join(list(d))))
    return values

def parse_lp(file):
    with open(file, 'r') as inp:
        s = 0
        Eqin = []
        a = []
        b = []
        for line in inp:
            if s == 0:
                if line.lower().startswith('min'):
                    r = parse('min {}', line.lower())
                    MinMax = -1
                elif line.lower().startswith('max'):
                    r = parse('max {}', line.lower())
                    MinMax = 1
                c = np.array(get_vars(r[0]))
                s+=1
            elif s == 1 or s == 2:
                if line.lower().startswith('s.t.'):
                    r = parse('s.t. {}', line)
                    rest = r[0]
                    s = 2
                else:
                    rest = line
                s = find_symbol(rest)
                if s == 0:
                    r = parse('{}={}', rest)
                elif s == -1:
                     r = parse('{}<={}', rest)
                elif s == 1:
                    r = parse('{}>={}', rest)
                Eqin.append(s)
                ax = get_vars(r[0])
                a.append(ax)
                v = r[1].strip()
                b.append(float(v))
            elif s == 3:
                b = np.array(b)
                a = np.array(a)
                Eqin = np.array(Eqin)
        return Eqin, a, b, c, MinMax