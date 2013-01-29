#!/usr/bin/env python
"""
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random

def hello(phenny, input): 
    greeting = random.choice(('Hi', 'Hey', 'Hello', 'What\'s kicking', 'What\'s the good word', 'Top of the morning', 'Yo', 'What up', "What's hanging", "In the hood", "Kaixo", "Zer moduz"))
    punctuation = random.choice(('', '!'))
    phenny.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey|what\'s kickin[\'g]*|how you been|what\'s (.*)good(.*)|top o[\'f]* the mornin[\'g]*|what\'s hangin[\'g]*|yo|in the hood|in da hoodi|kaixo|zer moduz) $nickname[ \t]*$'

def interjection(phenny, input): 
    phenny.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

if __name__ == '__main__': 
    print(__doc__.strip())
