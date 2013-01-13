#!/usr/bin/env python
"""
wikipedia.py - Phenny Wikipedia Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, urllib.request, urllib.parse, urllib.error, gzip, io
import wiki

wikiapi = 'https://%s.wikipedia.org/w/api.php?action=query&list=search&srsearch={0}&limit=1&prop=snippet&format=json'
wikiuri = 'https://%s.wikipedia.org/wiki/{0}'
wikisearch = 'https://%s.wikipedia.org/wiki/Special:Search?' \
                          + 'search={0}&fulltext=Search'

langs = ['ar', 'bg', 'ca', 'cs', 'da', 'de', 'en', 'es', 'eo', 'eu', 'fa', 'fr', 'ko', 'hi', 'hr', 'id', 'it', 'he', 'lt', 'hu', 'ms', 'nl', 'ja', 'no', 'pl', 'pt', 'kk', 'ro', 'ru', 'sk', 'sl', 'sr', 'fi', 'sv', 'tr', 'uk', 'vi', 'vo', 'war', 'zh']

def wik(phenny, input): 
    """Search for something on Wikipedia"""
    origterm = input.groups()[1].split(' ')
    
    lang = "en"
    if origterm[0] in langs:
        lang = origterm[0]
        origterm.pop(0)
    
    origterm = ' '.join(origterm)
    
    if not origterm: 
        return phenny.say('Perhaps you meant ".wik Zen"?')

    term = urllib.parse.unquote(origterm)
    term = urllib.parse.quote(origterm)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')

    w = wiki.Wiki(wikiapi % lang, wikiuri % lang, wikisearch % lang)

    try:
        result = w.search(term)
    except IOError: 
        error = "Can't connect to en.wikipedia.org ({0})".format(wikiuri.format(term))
        return phenny.say(error)
        
        
    if result is not None: 
        phenny.say(result)
    else:
        phenny.say('Can\'t find anything in Wikipedia for "{0}".'.format(origterm))

wik.commands = ['wik']
wik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
