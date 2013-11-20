#!/usr/bin/env python
"""
seen.py - Phenny Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import time, os, shelve
from tools import deprecated

def f_seen(phenny, input): 
    """.seen <nick> - Reports when <nick> was last seen."""
    nick = input.group(2).lower()
    if not hasattr(phenny, 'seen'): 
        return phenny.msg(input.sender, '?')
    if nick in phenny.seen: 
        channel, t = phenny.seen[nick]
        t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))

        msg = "I last saw %s at %s on %s" % (nick, t, channel)
        phenny.reply(msg)
    else: phenny.reply("Sorry, I haven't seen %s around." % nick)
f_seen.name = 'seen'
f_seen.example = '.seen firespeaker'
f_seen.rule = (['seen'], r'(\S+)')

@deprecated
def f_note(self, origin, match, args): 
    def note(self, origin, match, args): 
        if not hasattr(self.bot, 'seen'): 
            fn = self.nick + '-' + self.config.host + '.seen'
            path = os.path.join(os.path.expanduser('~/.phenny'), fn)
            self.bot.seen = shelve.open(path)
        if origin.sender.startswith('#'): 
            self.seen[origin.nick.lower()] = (origin.sender, time.time())
            self.seen.sync()

    try: note(self, origin, match, args)
    except Exception as e: print(e)
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__': 
    print(__doc__.strip())
