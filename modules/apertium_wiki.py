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

def format_subsection(section):
   section = section.replace(' ', '_')
   section = urllib.parse.quote(section)
   section = section.replace('%', '.')
   return section

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
   
   page = lxml.html.fromstring(html)

   if "#" in origterm:
      section = format_subsection(origterm.split("#")[1])
      text = page.find(".//span[@id='%s']" % section)
      if text is None:
         phenny.reply("That subsection does not exist.")
         return
      text = text.getparent().getnext()
   else:
      paragraphs = page.findall('.//p')
      if len(paragraphs) > 2:
        text = page.findall('.//p')[1]
      else:
        text = page.findall(".//*[@id='mw-content-text']")[0]

   sentences = text.text_content().split(". ")   
   sentence = '"' + sentences[0] + '"'
   
   maxlength = 430 - len(' - ' + wikiuri % (format_term_display(term)))
   if len(sentence.encode('utf-8')) > maxlength: 
      sentence = sentence[:maxlength]
      words = sentence[:-5].split(' ')
      words.pop()
      sentence = ' '.join(words) + ' [...]'

   phenny.say(sentence + ' - ' + wikiuri % (format_term_display(term)))

awik.commands = ['awik']
awik.example = '.awik Begiak'
awik.priority = 'high'