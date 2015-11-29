#!/usr/bin/python3
"""
weirdfun.py - activities that weird people do
author: firespeaker <firespeaker@firespeaker.org>
"""

import random

otherweird = "zfe"

def fight(phenny, input):
    """Have begiak fight someone for you."""
    global otherweird
    whouser = input.groups()[1]
    already = False
    if whouser:
        otherweird = whouser
        if whouser.lower()==phenny.nick.lower():
            already = True
            phenny.say("ouch!")

    #### "hits %s", "punches %s", "kicks %s",, "stabs %s with a clean kitchen knife",  "hits %s with a rubber hose",
    messages = [ "hurts himself by accident while trying to attack %s", "directs his Öflazers at %s", "is bored of violence against %s", "thinks you should talk it over with %s first", "cocks %s's beer", "eats %s's hat", "sets %s up the bomb"]
    response = random.choice(messages)

    if not already:
        phenny.do(response % otherweird)

fight.commands = ['fight']
fight.priority = 'low'
fight.example = '.fight ChanServ'

def hug(phenny, input):
    """Have begiak hug someone for you."""
    global otherweird
    whouser = input.groups()[1]
    if whouser:
        otherweird = whouser

    if not whouser:
        phenny.do('tries to hug himself but fails.')
    elif whouser.lower()==phenny.nick.lower():
        phenny.do("tries but fails.")
    else:
        phenny.do("hugs %s" % otherweird)

hug.commands = ['hug']
hug.priority = 'low'
hug.example = '.hug ChanServ'
if __name__ == '__main__':
    print(__doc__.strip())
