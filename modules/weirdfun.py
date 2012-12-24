#!/usr/bin/python3
"""
weirdfun.py - activities that weird people do
author: firespeaker <firespeaker@firespeaker.org>
"""

import random

otherbot = "zfe"

def botfight(phenny, input):
    global otherbot
    whouser = input.groups()[1]
    if whouser:
        otherbot = whouser
    #### "hits %s", "punches %s", "kicks %s",, "stabs %s with a clean kitchen knife",  "hits %s with a rubber hose",
    messages = [ "hurts himself by accident while trying to attack %s", "directs his Öflazers at %s", "is bored of violence against %s", "thinks you should talk it over with %s first", "cocks %s's beer"]
    response = random.choice(messages)

    phenny.do(response % otherbot)
botfight.commands = ['botfight']
botfight.priority = 'low'

def bothug(phenny, input):
    phenny.do("hugs %s" % otherbot)
bothug.commands = ['bothug']
bothug.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
