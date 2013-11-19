#!/usr/bin/python3
"""
ethnologue.py - Ethnologue.com language lookup
author: mattr555
"""

from .iso639 import ISOcodes
from lxml import html
import urllib.request
from urllib.error import HTTPError

def shorten_num(n):
    if n < 99999:
        return '{:,}'.format(n)
    elif n < 999999:
        return '{}K'.format(round(n/1000))
    elif n < 999999999:
        return '{}M'.format(round(n/1000000, 1))

def parse_num_speakers(s):
    hits = []
    for i in s.split(' '):
        if len(i) <= 3 or ',' in i:
            if i.replace(',', '').replace('.', '').isdigit():
                hits.append(int(i.replace(',', '').replace('.', '')))
    return shorten_num(hits[-1])

def ethnologue(phenny, input):
    """.ethnologue <lg> - gives ethnologue info from partial language name or iso639"""
    raw = str(input.group(2)).lower()
    iso = []
    if len(raw) == 3 and raw in ISOcodes:
        iso.append(raw)
    elif len(raw) > 3:
        for code, lang in ISOcodes.items():
            if raw in lang.lower():
                iso.append(code)

    if len(iso) == 1:
        url = "http://www.ethnologue.com/language/" + iso[0]
        try:
            resp = urllib.request.urlopen(url).read()
        except HTTPError as e:
            phenny.say('Oh noes! Ethnologue responded with ', e)
            return
        h = html.document_fromstring(resp)

        name = h.get_element_by_id('page-title').text
        iso_code = h.find_class('field-name-language-iso-link-to-sil-org')[0].find('div/div/a').text
        where_spoken = h.find_class('field-name-a-language-of')[0].find('div/div/h2/a').text
        where_spoken_cont = h.find_class('field-name-field-region')
        if where_spoken_cont:
            where_spoken_cont = where_spoken_cont[0].find('div/div/p').text[:100]
            if len(where_spoken_cont) > 98:
                where_spoken_cont += '...'
            where_spoken += ', ' + where_spoken_cont
        num_speakers_field = h.find_class('field-name-field-population')[0].find('div/div/p').text
        num_speakers = parse_num_speakers(num_speakers_field)

        response = "Ethnologue results for {} (ISO-639 code {}): spoken in {}. {} L1 speakers. Src: {}".format(name, iso_code, where_spoken, num_speakers, url)
    elif len(iso) > 1:
        did_you_mean = ['{} ({})'.format(i, ISOcodes[i]) for i in iso if len(i) == 3]
        response = "Did you mean: " + ', '.join(did_you_mean) + "? Use iso639 code for better results."
    else:
        response = "That ISO code wasn't found. (Hint: use .iso639 for better results)"

    phenny.say(response)

ethnologue.name = 'ethnologue'
ethnologue.commands = ['ethnologue']
ethnologue.example = '.ethnologue khk'
ethnologue.priority = 'low'
