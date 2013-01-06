#!/usr/bin/env python
"""
seen.py - Phenny Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import time
from tools import deprecated

def f_seen(phenny, input): 
    """.seen <nick> - Reports when <nick> was last seen."""
    if input.sender == '#talis': return
    nick = input.group(2).lower()
    if not hasattr(phenny, 'seen'): 
        return self.msg(input.sender, '?')
    if nick in phenny.seen: 
        channel, t = phenny.seen[nick]
        t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))

        msg = "I last saw %s at %s on %s" % (nick, t, channel)
        phenny.reply(msg)
    else: phenny.reply("Sorry, I haven't seen %s around." % nick)
f_seen.name = 'seen'
f_seen.example = '.seen firespeaker'
f_seen.rule = (['seen'], r'(\S+)')


def f_note(phenny, input): 
    def note(phenny, input): 
        if not hasattr(phenny.bot, 'seen'): 
            phenny.bot.seen = {}
        if input.sender.startswith('#'): 
            # if origin.sender == '#inamidst': return
            phenny.seen[input.nick.lower()] = (input.sender, time.time())

        # if not hasattr(self, 'chanspeak'): 
        #     self.chanspeak = {}
        # if (len(args) > 2) and args[2].startswith('#'): 
        #     self.chanspeak[args[2]] = args[0]

    try: note(phenny, input)
    except Exception as e: print(e)
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__': 
    print(__doc__.strip())
