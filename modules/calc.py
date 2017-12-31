#!/usr/bin/env python
# coding=utf-8
"""
calc.py - Phenny Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web
import sympy
import re

def c(phenny, input):
    if not input.group(2):
        return phenny.reply("Nothing to calculate.")
    calc = input.group(2)

    if '=' in calc:
        calc = calc.replace(' ', '')
        calc = re.sub(r"((?:\d+)|(?:[a-zA-Z]\w*\(\w+\)))((?:[a-zA-Z]\w*)|\()", r"\1*\2", calc)

        left, right = calc.split('=')
        calc = left + '-(' + right + ')'
        try:
            result = sympy.solve(calc)
        except:
            return phenny.say('Sorry, no result.')

    else:
        try:
            result = sympy.sympify(calc)
        except:
            return phenny.say('Sorry, no result.')

    res = ''
    more = False
    if type(result) is list and len(result) > 1:
        if type(result[0]) is not dict:
            more = True
            for element in result:
                res += str(sympy.N(element)) + ', '
            res = res[:-2]
            res = '[' + res + ']'
    elif type(result) is list and len(result) == 1:
        result = result[0]

    if more is not True:
        try:
            result = str(float(result))
            if result.endswith('.0'):
                result = str(int(float(result)))
        except:
            result = str(result)
            if result.isalpha():
                return phenny.say('Sorry, no result.')

        if result:
            phenny.say(result)
        else:
            return phenny.say('Sorry, no result.')
    else:
        phenny.say(res)
    
c.commands = ['c']
c.example = '.c 5 + 3'

def py(phenny, input): 
   """evaluates a python2 expression via a remote sandbox"""
   query = input.group(2).encode('utf-8')
   uri = 'http://tumbolia.appspot.com/py/'
   answer = web.get(uri + web.quote(query))
   if answer: 
      phenny.say(answer)
   else: phenny.reply('Sorry, no result.')
py.commands = ['py']
py.example = '.py if not False: print "hello world!"'

if __name__ == '__main__':
    print(__doc__.strip())
