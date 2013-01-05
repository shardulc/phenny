#!/usr/bin/python3
"""
weirdfun.py - activities that weird people do
author: firespeaker <firespeaker@firespeaker.org>
"""

import random

otherbot = "zfe"

def weirdfight(phenny, input):
    """Have begiak fight someone for you."""
    global otherbot
    whouser = input.groups()[1]
    already = False
    if whouser:
        otherbot = whouser
        if whouser.lower()=="begiak":
            already = True
            phenny.say("ouch!")

    #### "hits %s", "punches %s", "kicks %s",, "stabs %s with a clean kitchen knife",  "hits %s with a rubber hose",
    messages = [ "hurts himself by accident while trying to attack %s", "directs his Öflazers at %s", "is bored of violence against %s", "thinks you should talk it over with %s first", "cocks %s's beer"]
    response = random.choice(messages)

    if not already:
        phenny.do(response % otherbot)

weirdfight.commands = ['fight']
weirdfight.priority = 'low'
weirdfight.example = '.fight ChanServ'

def weirdhug(phenny, input):
    """Have begiak hug someone for you."""
    phenny.do("hugs %s" % otherbot)
weirdhug.commands = ['hug']
weirdhug.priority = 'low'
weirdhug.example = '.hug ChanServ'
if __name__ == '__main__':
    print(__doc__.strip())
