#!/usr/bin/env python
"""
away.py - Phenny's record or who's away/present module
"""

import os, re, time, random
import web

statuses = {"alan": "boom bitchezzzz"}

def debug(phenny, input):
	phenny.say(str(statuses))
debug.commands = ['debug']

def whereis(phenny, input):
	"""Tells you nick's current status."""
	whereis_nick = input.split(" ")[1]
	print(input + " --> " + whereis_nick)
	if (whereis_nick in list(statuses.keys())):
		phenny.reply(whereis_nick + " said: " + statuses[whereis_nick])
	else:
		phenny.reply("Sorry, " + whereis_nick + " seems to be AWOL...")
whereis.commands = ["whereis"]
whereis.priority = 'low'
whereis.example = '.whereis sushain'
whereis.thread = False


def update_status(phenny, input):
	nick = input.nick
	if input.count(" ") == 0:
		if input == ".away":
			statuses[nick] = "I'm away right now"
		else:
			statuses[nick] = "I'm around at the minute"
	else:
		message = str(" ".join(input.split(" ")[1:]))
		statuses[nick] = message


update_status.commands = ["away", "back"]
update_status.priority = 'low'
update_status.thread = False


if __name__ == '__main__': 
    print(__doc__.strip())
