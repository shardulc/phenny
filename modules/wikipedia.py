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

def format_term(term):
    term = urllib.parse.unquote(term)
    term = urllib.parse.quote(term)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')
    return term

def wikipedia(phenny, origterm, lang):
    origterm = origterm.strip()
    lang = lang.strip()

    if not origterm: 
        return phenny.say('Perhaps you meant ".wik Zen"?')

    term = format_term(origterm)

    w = wiki.Wiki(wikiapi % lang, wikiuri % lang, wikisearch % lang)

    try:
        result = w.search(term)
    except IOError: 
        error = ("Can't connect to %s.wikipedia.org ({0})" % lang).format((wikiuri % lang).format(urllib.parse.unquote(term)))
        return phenny.say(error)
        
        
    if result is not None: 
        phenny.say(result)
    else:
        phenny.say('Can\'t find anything in Wikipedia for "{0}".'.format(origterm))

def wik(phenny, input): 
    """Search for something on Wikipedia"""
    origterm = input.group(1)
    lang = "en"
    
    m = re.match(r'\.wik\.([a-z]{2,3})(?: +(.*))', input.group(0))
    if m:
        lang = m.group(1)
        origterm = m.group(2)
        
    wikipedia(phenny, origterm, lang)
wik.rule = r'\.wik(?:(.*))'
wik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())