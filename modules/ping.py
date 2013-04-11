#!/usr/bin/env python
"""
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random, re

def hello(phenny, input): 
    nickname = phenny.nick
    temporaryMessage = "  If you're a GSoC student, check out http://wiki.apertium.org/wiki/Top_tips_for_GSOC_applications"
    greeting = random.choice(('Hi', 'Hey', 'Hello', 'What\'s kicking', 'What\'s the good word', 'Top of the morning', 'Yo', 'What up', "What's hanging", "In the hood", "Kaixo", "Zer moduz", "Сәлем", "Қалың қалай", "Salom", "Привет", "No bugs is good bugs", "Mitä kuuluu", "حالت چطوره", "როგორა ხარ", "ինչպե՞ս ես", "сайн байна уу", "कैसे हो", "Como vai", "Nasılsın"))
    if not re.search(nickname, input):
        punctuation = random.choice(('.', '!', ';'))
        phenny.say(greeting + ' ' + input.nick + punctuation +temporaryMessage)
    else:
        punctuation = random.choice(('', '!'))
        phenny.say(greeting + ' ' + input.nick + punctuation)


#hello.rule = r'(?i)(hi|hello|hey|what\'s kickin[\'g]*|how you been|what\'s (.*)good(.*)|top o[\'f]* the mornin[\'g]*|what\'s hangin[\'g]*|yo|in the hood|in da hood|kaixo|zer moduz|с[әа]л[еао]м|wb) $nickname[ \t]*$'
#strings = "(?i)(hi|hello|hey|what\'s kickin[\'g]*|how you been|what\'s (.*)good(.*)|top o[\'f]* the mornin[\'g]*|what\'s hangin[\'g]*|yo|in the hood|in da hood|kaixo|zer moduz|с[әа]л[еао]м|s[ae]l[ao]m|wb)"
hello.rule = r'(?:$nickname[,:]* )?(?i)(hi|hello|hey|what\'s kickin[\'g]*|how you been|what\'s (.*)good(.*)|what\'s up[\.!\?]*|(?:top o[\'f]* the )?mornin[\'g]*|what\'s hangin[\'g]*|yo|in the hood|in da hood|kaixo|zer moduz|с[әа]л[еао]м|s[ae]l[ao]m|wb|mitä kuuluu|როგორა ხარ|ինչպե՞ս ես|сайн байна уу|कैसे हो|como vai|nasılsın(?:ız)?)(?:[,]* $nickname)?[ \t]*$'

def interjection(phenny, input): 
    phenny.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

if __name__ == '__main__': 
    print(__doc__.strip())
