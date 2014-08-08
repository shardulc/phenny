#!/usr/bin/python3
"""
botfun.py - activities that bots do
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

def noexceptions(phenny, input):
   """Tells someone there aren't ever any exceptions"""
   #whouser = input.groups()[1]
   whouser = input.nick
   if not whouser:
      return phenny.say('NO EXCEPTIONS!')

   response = "NO EXCEPTIONS, %s!"
   phenny.say(response % whouser)

#noexceptions.commands = ['noexceptions']
#noexceptions.example = '.noexceptions firespeaker'
noexceptions.rule = r'.*(?i)((no|any|most|some|other|many|lot of|few|several|certain|никак.*|нет) (exception|исключени)).*$'
noexceptions.priority = 'low'

def harglebargleP(phenny, input):
   """Tells someone hargle bargle (cf. http://nedroidcomics.livejournal.com/224029.html , http://quotes.firespeaker.org/?id=1415)"""
   whouser = input.groups()[1]
   if not whouser:
      return phenny.say('HARGLE BARGLE!')
   response = "HARGLE BARGLE, %s!"
   phenny.say(response % whouser)

harglebargleP.commands = ['harglebargle']
harglebargleP.example = '.harglebargle firespeaker'
harglebargleP.priority = 'low'

def bargle(phenny, input):
   """Says bargle if someone says hargle (cf. http://nedroidcomics.livejournal.com/224029.html , http://quotes.firespeaker.org/?id=1415)"""
   if input != "hargle bargle" and input != "harglebargle":
      phenny.say("bargle!")

bargle.rule = r'.*(?i)(hargle).*$'
bargle.priority = 'low'

def hargle(phenny, input):
   """Says harglebargle if someone says bargle (cf. http://nedroidcomics.livejournal.com/224029.html , http://quotes.firespeaker.org/?id=1415)"""
   if input != "hargle bargle" and input != "harglebargle":
      phenny.say("HARGLE BARGLE!")

hargle.rule = r'.*(?i)(bargle).*$'
hargle.priority = 'low'



def harglebargle(phenny, input):
   """Says hargle bargle if someone says hargle bargle (cf. http://nedroidcomics.livejournal.com/224029.html , http://quotes.firespeaker.org/?id=1415)"""
   phenny.say('HARGLE BARGLE!')

harglebargle.example = '.harglebargle firespeaker'
harglebargle.priority = 'low'
harglebargle.rule = r'.*(?i)(hargle[\s]*bargle).*$'

if __name__ == '__main__':
   print(__doc__.strip())

def udmurt(phenny, input):
   """expresses joy over mention of Udmurt"""
   phenny.say("\o/ \o/ \o/ U D M U R T \o/ \o/ \o/")

udmurt.rule = r'.*(?i)(udmurt).*$'
udmurt.priority = 'low'

def particles(phenny, input):
   """expresses sadness over mention of particles"""
   message = "this is my particles face :((((("
   whouser = input.nick
   if not whouser:
      phenny.say(message)
   else:
      phenny.say("%s: %s" % (whouser, message))

particles.rule = r'.*(?i)(particle|частиц|partikkel).*$'
particles.priority = 'low'
