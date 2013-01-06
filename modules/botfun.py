#!/usr/bin/python3
"""
botfun.py - activities that bots do
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

otherbot = "ChanServ"

def botfight(phenny, input):
    """Make begiak fight other bots in the room."""
    messages = ["hits %s", "punches %s", "kicks %s", "hits %s with a rubber hose", "stabs %s with a clean kitchen knife"]
    response = random.choice(messages)

    phenny.do(response % otherbot)
botfight.commands = ['botfight']
botfight.priority = 'low'
botfight.example = '.botfight'

def bothug(phenny, input):
    """Make begiak hug other bots in the room."""
    phenny.do("hugs %s" % otherbot)
bothug.commands = ['bothug']
bothug.priority = 'low'
bothug.example = '.bothug'

if __name__ == '__main__':
    print(__doc__.strip())