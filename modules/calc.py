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

subs = [
    ('£', 'GBP '),
    ('€', 'EUR '),
    ('\$', 'USD '),
    (r'\n', '; '),
    ('&deg;', '°'),
    (r'\/', '/'),
]


def c(phenny, input):
    if not input.group(2):
        return phenny.reply("Nothing to calculate.")
    calc = input.group(2)

    if '=' in calc:
        calc = calc.replace(' ', '')
        symbols = ''
        for c in calc:
            if c.isalpha() and c not in symbols:
                symbols += c + ' '
        symbols = symbols[:-1]

        left, right = calc.split('=')
        calc = left + '-(' + right + ')'
        try:
            result = str(float(sympy.solve(calc, sympy.Symbol(symbols))[0]))
        except:
            return phenny.say('Sorry, no result.')

    else:
        try:
            result = str(float(sympy.sympify(calc)))
        except:
            return phenny.say('Sorry, no result.')

    if result:
        phenny.say(result)
    else:
        phenny.reply('Sorry, no result.')
    
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

def wa(phenny, input): 
    """Query Wolfram Alpha."""

    if not input.group(2):
        return phenny.reply("No search term.")
    query = input.group(2)

    re_output = re.compile(r'{"stringified": "(.*?)",')

    uri = 'http://www.wolframalpha.com/input/?i={}'
    out = web.get(uri.format(web.quote(query)))
    answers = re_output.findall(out)
    if len(answers) <= 0:
        phenny.reply("Sorry, no result.")
        return

    answer = answers[1]
    for sub in subs:
        answer = answer.replace(sub[0], sub[1])

    phenny.say(answer)
wa.commands = ['wa']
wa.example = '.wa answer to life'

if __name__ == '__main__':
    print(__doc__.strip())
