#!/usr/bin/env python
"""
pester.py - Phenny's pester module
"""

import os, re, time, random, datetime
import web

SECONDS_TO_PESTER = 5
POSTPONE_SECONDS = 10

def pester(phenny, input):
	""".pester <user> to <mess> - Starts a pester"""
	user = input.group(2)
	mess = input.group(3)
	
	if (not user) or (not mess):
		phenny.say(pester_postpone.__doc__.strip())
		return
	user = user.lower()
	
	if not (user in phenny.pesters):
		phenny.pesters[user] = [{'origin-user':input.nick.lower(), 'message':mess, 'time-thold':datetime.datetime.now()}]
	else:
		phenny.pesters[user].append({'origin-user':input.nick.lower(), 'message':mess, 'time-thold':datetime.datetime.now()})	
	phenny.say("OK " + input.nick + ", I will pester " + input.group(2) + " to " +  input.group(3))	
pester.rule = (['pester'], r'(.*)\sto\s(.*)')
pester.priority = 'high'
pester.example = '.pester user_xyz to commit his code :)'

def stop_pester(phenny,input):
    """.stoppestering <user> to <mess> - Stops a pester"""
    user = input.group(2)
    mess = input.group(3)
    
    if (not user) or (not mess):
        phenny.say(stop_pester.__doc__.strip())
        return
    user = user.lower()
    
    success = False
    if (user in list(phenny.pesters.keys())):
        for pest in (phenny.pesters[user])[:]:
            if (pest['origin-user'] == input.nick.lower()) and (pest['message'] == mess):
                phenny.pesters[user].remove(pest)
                success = True
    else:
        phenny.say(input.nick.lower() + ": Looks like " + user + " does not have any pesters from you...")
        return
    if success:
        phenny.say(input.nick.lower() + ": Successfully deleted pesters.")
    else:
        success = False
        for pest in phenny.pesters[input.nick.lower()]:
            if (pest['origin-user'] == input.nick.lower()):
                phenny.say(input.nick.lower() + ": Perhaps did you mean: .stoppestering " + user + " to " + pest['message'])
                success = True
        if not success:
            phenny.say(input.nick.lower() + ": Looks like " + user + " does not have any pesters from you...")
    
stop_pester.rule = (['stoppestering'], r'(.*)\sto\s(.*)')
stop_pester.priority = 'high'
stop_pester.example = '.stoppestering user_xyz to commit his code :)'

def pester_alert(phenny, input):
    success = False	
    if (input.nick.lower() in list(phenny.pesters.keys())):
        for pest in phenny.pesters[input.nick.lower()]:
            if pest['time-thold'] <= datetime.datetime.now():
                success = True
                phenny.say(input.nick.lower() + ": <" + pest['origin-user'] + "> " + pest['message'])
                pest['time-thold'] = datetime.datetime.now() + datetime.timedelta(0,SECONDS_TO_PESTER)
    if not success:
        phenny.say("No pesters for you!") #Debug
	
# pester_alert.event = 'JOIN' #Uncomment for non-debug
pester_alert.commands = ['getpesters'] #Debug
pester_alert.priority = 'high'
pester_alert.thread = False

def pester_postpone(phenny,input):
    """.postponepester from <user> - Postpone a pester"""
    user = input.group(2).strip()
    
    if not user:
        phenny.say(pester_postpone.__doc__.strip())
        return
    user = user.lower()
    
    success = False
    if (input.nick.lower() in list(phenny.pesters.keys())):
        for pest in (phenny.pesters[input.nick.lower()]):
            if (pest['origin-user'] == user):
                pest['time-thold'] = datetime.datetime.now() + datetime.timedelta(0,POSTPONE_SECONDS)
                success = True
    else:
        phenny.say(input.nick.lower() + ": Looks like you are not being pestered :P")
        return
    if success:
        phenny.say(input.nick.lower() + ": Successfully postponed pesters.")
    else:
        phenny.say(input.nick.lower() + ": Looks like " + user + " is not pestering you...")

pester_postpone.rule = (['postponepester'], r'from\s(.*)')
pester_postpone.priority = 'high'
pester_postpone.example = '.postponepester from vigneshv'

def pester_dismiss(phenny,input):
    """.dismisspester from <user> - Dismiss a pester"""
    user = input.group(2)
    
    if not user:
        phenny.say(pester_dismiss.__doc__.strip())
        return
    user = user.lower()
    
    success = False
    if (input.nick.lower() in list(phenny.pesters.keys())):
        for pest in (phenny.pesters[input.nick.lower()])[:]:
            if (pest['origin-user'] == user):
                phenny.pesters[user].remove(pest)
                success = True
    else:
        phenny.say(input.nick.lower() + ": Looks like you are not being pestered :P")
        return
    if success:
        phenny.say(input.nick.lower() + ": Successfully dismissed pesters.")
    else:
        phenny.say(input.nick.lower() + ": Looks like " + user + " is not pestering you...")
        
        
def setup(phenny):
	phenny.pesters = {}


if __name__ == '__main__': 
    print(__doc__.strip())