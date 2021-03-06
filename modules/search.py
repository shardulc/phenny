#!/usr/bin/env python
"""
search.py - Phenny Web Search Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web
import requests
from tools import truncate
from modules import more
from web import catch_timeout, is_up, REQUEST_TIMEOUT

ddg_uri = 'https://api.duckduckgo.com/?format=json&pretty=1&q='
suggest_uri = 'http://suggestqueries.google.com/complete/search?client=firefox&hl=en&q='

def gsearch(phenny, input):
    phenny.reply('.g is deprecated. Try .search powered by Duck Duck Go instead.')
gsearch.commands = 'g'

def topics(phenny, input):
    if not is_up('https://api.duckduckgo.com'):
        return phenny.say('Sorry, DuckDuckGo API is down.')

    if not input.group(2): 
        return phenny.reply('.topics about what?')
    query = input.group(2)

    r = requests.get(ddg_uri + query, timeout=REQUEST_TIMEOUT).json()
    topics = r['RelatedTopics']
    if len(topics) == 0:
        return phenny.say('Sorry, no topics found.')
    topics_list = []
    counter = 0
    for topic in r['RelatedTopics'][:10]:
        try:
            topics_list.append(topic['Text'] + ' - ' + topic['FirstURL'])
        except KeyError:
            continue
    phenny.say(topics_list[0])
    phenny.reply('Check PM for more topics.')
    more.add_messages(phenny, input.nick, topics_list[1:])
topics.commands = ['topics']

def search(phenny, input):
    if not input.group(2): 
        return phenny.reply('.search for what?')
    query = input.group(2)

    if not is_up('https://api.duckduckgo.com'):
        return phenny.say('Sorry, DuckDuckGo API is down.')

    r = requests.get(ddg_uri + query, timeout=REQUEST_TIMEOUT).json()
    try:
        answer = r['AbstractText']
        answer_url = r['AbstractURL']
        if answer == '':
            answer = r['RelatedTopics'][0]['Text']
            answer_url = r['RelatedTopics'][0]['FirstURL']
            if answer == '':
                return phenny.say('Sorry, no result.')
    except:
        return phenny.say('Sorry, no result.')
    # Removes html tags, if exist
    answer = re.sub('<.+?>', '', answer)
    phenny.say(truncate(answer, share=' - ' + r['AbstractURL']) + ' - ' + answer_url)
search.commands = ['search']

def suggest(phenny, input):
    ''' Shows first 10 results from Google Suggestion API.'''
    if not input.group(2):
        return phenny.reply("No query term.")
    query = input.group(2)
    answer = requests.get(suggest_uri + query)
    suggestions = answer.json()[1][:10]
    phenny.reply(suggestions[0])
    phenny.reply('Check PM for more.')
    more.add_messages(phenny, input.nick, suggestions[1:])
suggest.commands = ['suggest']

def lmgtfy(phenny, input):
    if not input.group(2):
        phenny.reply('.lmgtfy what f who?')
    try:
        (who, what) = input.group(2).split(' ', 1)
        response = "%s: http://lmgtfy.com/?q=%s"
        what = web.quote(what)
        phenny.say(response % (who, what))
    except ValueError:
        phenny.reply('.lmgtfy what for who? (enter a nick and a query)')
lmgtfy.commands = ['lmgtfy']

if __name__ == '__main__': 
    print(__doc__.strip())
