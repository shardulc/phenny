#!/usr/bin/env python
"""
clock.py - Phenny Clock Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import math
import time
import locale
import socket
import struct
import datetime
import web
import pytz
from decimal import Decimal as dec
from tools import deprecated


r_local = re.compile(r'\([a-z]+_[A-Z]+\)')

def f_time(phenny, input): 
    """.time [timezone|offset] Returns current time in defined timezone/offset. Defaults to GMT."""
    d = datetime.datetime.utcnow()
    d = d.replace(tzinfo=pytz.utc)
    tz = input.group(2) or 'GMT'
    TZ = tz.upper()
    tz_nodel = tz.replace(':', '').replace('.', '')

    if (TZ == 'UTC') or (TZ == 'Z'):
        phenny.reply(d.strftime('%Y-%m-%dT%H:%M:%SZ'))
    elif TZ in pytz.all_timezones:
        TZ = pytz.timezone(TZ)
        phenny.reply(d.astimezone(TZ).strftime('%a, %d %b %Y %H:%M:%S %Z'))
    elif tz[0] in ('+', '-') and 3 <= len(tz_nodel) <= 5 and tz_nodel[1:].isdigit() and len(tz) - len(tz_nodel) <= 1:
        if 2 <= tz.find(':') <= 3:
            pos = tz.find(':')
            if int(tz[1:pos]) <= 24 and int(tz[pos+1:]) <= 59:
               offset = int(tz[1:pos]) + int(tz[pos+1:]) / 60
            else:
                phenny.reply("Offset '%s' is invalid." %tz)
                return

        elif len(tz) - len(tz_nodel) == 0:
            if int(tz[1:-2]) <= 24 and int(tz[-2:]) <= 59:
                offset = int(tz[1:-2]) + int(tz[-2:]) / 60
            else:
                phenny.reply("Offset '%s' is invalid." %tz)
                return
        else:
            if float(tz[1:]) <= 24:
                offset = float(tz[1:])
            else:
               phenny.reply("Offset '%s' is invalid." %tz)
               return
        if tz[0] == '-':
            offset *= -1
        timenow = time.gmtime(time.time() + offset * 3600)
        phenny.reply (time.strftime('%a, %d %b %Y %H:%M:%S ' + str(tz), timenow))
    else:
        phenny.reply("Sorry, I don't know about the '%s' timezone." %tz)
f_time.name = 'time'
f_time.commands = ['time']
f_time.example = '.time UTC, .time +0100, .time -5:30, .time +8.75'

def beats(phenny, input): 
    """Shows the internet time in Swatch beats."""
    beats = ((time.time() + 3600) % 86400) / 86.4
    beats = int(math.floor(beats))
    phenny.say('@%03i' % beats)
beats.commands = ['beats']
beats.priority = 'low'

def divide(input, by): 
    return (input // by), (input % by)

def yi(phenny, input): 
    """Shows whether it is currently yi or not."""
    quadraels, remainder = divide(int(time.time()), 1753200)
    raels = quadraels * 4
    extraraels, remainder = divide(remainder, 432000)
    if extraraels == 4: 
        return phenny.say('Yes! PARTAI!')
    elif extraraels == 3:
    	  return phenny.say('Soon...')
    else: phenny.say('Not yet...')
yi.commands = ['yi']
yi.priority = 'low'

def tock(phenny, input): 
    """Shows the time from the USNO's atomic clock."""
    info = web.head('http://tycho.usno.navy.mil/cgi-bin/timer.pl')
    phenny.say('"' + info['Date'] + '" - tycho.usno.navy.mil')
tock.commands = ['tock']
tock.priority = 'high'

def npl(phenny, input): 
    """Shows the time from NPL's SNTP server."""
    # for server in ('ntp1.npl.co.uk', 'ntp2.npl.co.uk'): 
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b'\x1b' + 47 * b'\0', ('ntp1.npl.co.uk', 123))
    data, address = client.recvfrom(1024)
    if data: 
        buf = struct.unpack('B' * 48, data)
        d = dec('0.0')
        for i in range(8):
            d += dec(buf[32 + i]) * dec(str(math.pow(2, (3 - i) * 8)))
        d -= dec(2208988800)
        a, b = str(d).split('.')
        f = '%Y-%m-%d %H:%M:%S'
        result = datetime.datetime.fromtimestamp(d).strftime(f) + '.' + b[:6]
        phenny.say(result + ' - ntp1.npl.co.uk')
    else: phenny.say('No data received, sorry')
npl.commands = ['npl']
npl.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
