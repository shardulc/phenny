#!/usr/bin/python3
"""
randomquote.py - urban dictionary module
author: jonorthwash <jonorthwash@users.sourceforge.net>
"""

import urllib.request
from urllib.error import HTTPError
from tools import GrumbleError
import web
import json

#FIXME: need to implement
#def quote(phenny, input):
#    """.quote <id> - Get a quote from quotes.firespeaker.org."""
#
#    word = input.group(2)
#    if not word:
#        phenny.say(fs_quotes.__doc__.strip())
#        return
#    # create opener
#    opener = urllib.request.build_opener()
#    opener.addheaders = [
#        ('User-agent', web.Grab().version),
#        ('Referer', "http://quotes.firespeaker.org"),
#    ]
#
#    try:
#        req = opener.open("http://api.urbandictionary.com/v0/define?term={0}"
#                .format(web.quote(word)))
#        data = req.read().decode('utf-8')
#        data = json.loads(data)
#    except (HTTPError, IOError, ValueError):
#        raise GrumbleError(
#                "Urban Dictionary slemped out on me. Try again in a minute.")
#
#    if data['result_type'] == 'no_results':
#        phenny.say("No results found for {0}".format(word))
#        return
#
#    result = data['list'][0]
#    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(web.quote(word))
#
#    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
#    phenny.say(response)

def randquote(phenny, input):
    """.randquote (<topic>) - Get a random short quote from quotes.firespeaker.org (about topic)."""


    topic = input.group(2)

    # create opener
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent', web.Grab().version),
        ('Referer', "http://quotes.firespeaker.org/"),
    ]

    maxlen = 200

    try:
        if topic == "" or topic==None:
            req = opener.open("http://quotes.firespeaker.org/random.php?len=%s" % maxlen)
        else:
            req = opener.open("http://quotes.firespeaker.org/random.php?len=%s&topic=%s" % (maxlen,web.quote(topic)))
        data = req.read().decode('utf-8')
        data = json.loads(data)
    except (HTTPError, IOError, ValueError):
        raise GrumbleError(
                "Firespeaker.org down?  Try again later.")

    if len(data) == 0:
        phenny.say("No results found")
        return

    #result = data['list'][0]
    #url = 'http://www.urbandictionary.com/define.php?term={0}'.format(web.quote(word))
    #
    #response = "{0} - {1}".format(result['definition'].strip()[:256], url)

    if data['quote'] != None:
        quote = data['quote'].replace('</p>', '').replace('<p>', '').replace('\n', '  ').replace('<em>', '_').replace('</em>', '_').replace('&mdash;', '—')
        response = quote+" - "+data['short_url']
    else:
        phenny.say("Sorry, no quotes returned!")
        return

    phenny.say(response)
randquote.name = 'randquote'
randquote.commands = ['randquote']
randquote.example = '.randquote (linguistics)'
randquote.priority = 'low'

#urbandict.rule = (['urb'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
