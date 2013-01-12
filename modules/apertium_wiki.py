#!/usr/bin/env python
"""
apertium_wiki.py - Phenny Wikipedia Module
"""

import re, urllib.request, urllib.parse, urllib.error, gzip, io
import web
from lxml import etree
import lxml.html
import lxml.html.clean

wikiuri = 'http://wiki.apertium.org/wiki/%s'

def format_term(term):
   term = urllib.parse.quote(term)
   term = term[0].upper() + term[1:]
   term = term.replace(' ', '_')
   return term
   
def format_term_display(term):
   term = urllib.parse.unquote(term)
   term = term[0].upper() + term[1:]
   term = term.replace(' ', '_')
   return term
   
def awik(phenny, input):
   """Search for something on Apertium wiki."""
   origterm = input.groups()[1]
   if not origterm: 
      return phenny.say('Perhaps you meant ".wik Zen"?')
   #origterm = origterm.encode('utf-8')

   term = format_term(origterm)
   
   try:
      html = str(web.get(wikiuri % (term)))
   except:
      phenny.reply("A wiki page does not exist for that term.")
      return
   
   sentences = re.split(r' *[\.\?!]['"\)\]]* *', lxml.html.fromstring(html).findall('.//p')[1].text_content())
   
   sentence = '"' + sentences[0] + '"'
   
   maxlength = 440 - len(' - ' + wikiuri % (format_term_display(term)))
   if len(sentence.encode('utf-8')) > maxlength: 
      sentence = sentence[:maxlength]
      words = sentence[:-5].split(' ')
      words.pop()
      sentence = ' '.join(words) + ' [...]'
   
   phenny.say(sentence + ' - ' + wikiuri % (format_term_display(term)))

awik.commands = ['awik']
awik.example = '.awik Begiak'
awik.priority = 'high'