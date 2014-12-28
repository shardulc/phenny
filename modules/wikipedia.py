#!/usr/bin/env python
"""
wikipedia.py - Phenny Wikipedia Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, urllib.parse, wiki
from lxml import etree
import lxml.html
import lxml.html.clean
import web

wikiapi = 'https://%s.wikipedia.org/w/api.php?action=query&list=search&srsearch={0}&limit=1&prop=snippet&format=json'
wikiuri = 'https://%s.wikipedia.org/wiki/{0}'
wikisearch = 'https://%s.wikipedia.org/wiki/Special:Search?' \
                          + 'search={0}&fulltext=Search'

langs = ['ar', 'bg', 'ca', 'cs', 'da', 'de', 'en', 'es', 'eo', 'eu', 'fa', 'fr', 'ko', 'hi', 'hr', 'id', 'it', 'he', 'lt', 'hu', 'ms', 'nl', 'ja', 'no', 'pl', 'pt', 'kk', 'ro', 'ru', 'sk', 'sl', 'sr', 'fi', 'sv', 'tr', 'uk', 'vi', 'vo', 'war', 'zh']

def format_term(term):
    term = web.unquote(term)
    term = web.quote(term)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')
    return term

def format_term_display(term):
   term = web.unquote(term)
   term = term[0].upper() + term[1:]
   term = term.replace(' ', '_')
   return term

def format_subsection(section):
   section = section.replace(' ', '_')
   section = urllib.parse.quote_plus(section)
   section = section.replace('%', '.')
   section = section.replace(".3A", ":")
   return section

def parse_wiki_page(url, term, section = None):
    try:
        web_url = web.quote(url).replace("%3A", ":", 1)
        html = str(web.get(web_url))
    except:
        return "A wiki page does not exist for that term."
    page = lxml.html.fromstring(html)
    if section is not None:
        text = page.find(".//span[@id='%s']" % section)

        if text is None:
            return "That subsection does not exist."
        text = text.getparent().getnext()

        #a div tag may come before the text
        while text.tag is not None and text.tag != "p":
            text = text.getnext()
        url += "#" + format_term_display(section)
    else:
        #Get first paragraph

        text = page.get_element_by_id('mw-content-text').find('p')

    sentences = text.text_content().split(". ")   
    sentence = '"' + sentences[0] + '"'

    maxlength = 430 - len((' - ' + url).encode('utf-8'))
    if len(sentence.encode('utf-8')) > maxlength: 
        sentence = sentence.encode('utf-8')[:maxlength].decode('utf-8', 'ignore')
        words = sentence[:-5].split(' ')
        words.pop()
        sentence = ' '.join(words) + ' [...]'

    return sentence + ' - ' + url

def wikipedia(phenny, origterm, lang):
    origterm = origterm.strip()
    lang = lang.strip()

    if not origterm: 
        return phenny.say('Perhaps you meant ".wik Zen"?')
    
    section = None

    if "#" in origterm:
        origterm, section = origterm.split("#")[:2]
        section = format_subsection(section)
    term = format_term(origterm)

    w = wiki.Wiki(wikiapi % lang, wikiuri % lang, wikisearch % lang)

    try:
        result = w.search(term)
    except web.ConnectionError:
        error = "Can't connect to en.wikipedia.org ({0})".format(wikiuri.format(term))
        return phenny.say(error)

    if result is not None: 
        #Disregarding [0], the snippet
        url = result.split("|")[-1]
        phenny.say(parse_wiki_page(url, term, section))
            
    else:
        phenny.say('Can\'t find anything in Wikipedia for "{0}".'.format(origterm))

def wik(phenny, input): 
    """Search for something on Wikipedia"""
    origterm = input.group(3)
    if input.group(2):
        lang = input.group(2)
    else:
        lang = "en"

    wikipedia(phenny, origterm, lang)
wik.rule = r'\.(wik|wiki|wikipedia)(\.[a-z]{2,3})?\s(.*)'
#wik.commands = ['wik', 'wiki', 'wikipedia']
wik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
