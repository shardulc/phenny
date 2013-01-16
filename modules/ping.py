#!/usr/bin/env python
"""
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random

def hello(phenny, input): 
    greeting = random.choice(('Hi', 'Hey', 'Hello', 'What\'s kicking', 'What\'s good', 'Top of the morning', 'Yo', 'What up'))
    punctuation = random.choice(('', '!'))
    phenny.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey|what\'s kickin|how you been|what\'s good|top o\' the mornin|yo) $nickname[ \t]*$'

def interjection(phenny, input): 
    phenny.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

if __name__ == '__main__': 
    print(__doc__.strip())
