#!/usr/bin/python3
"""
botfun.py - activities that bots do
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

def noexceptions(phenny, input):
   whouser = input.groups()[1]
   if not whouser:
      return phenny.say('NO EXCEPTIONS!')

   response = "NO EXCEPTIONS, %s!"
   phenny.say(response % whouser)

noexceptions.commands = ['noexceptions']
noexceptions.priority = 'low'

if __name__ == '__main__':
   print(__doc__.strip())
