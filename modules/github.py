#!/usr/bin/env python
"""
github.py - Github Post-Receive Hooks Module
"""

import http.server
import socketserver
import urllib.parse
import json

PORT = 1234

Handler = None
httpd = None

class MyHandler(http.server.SimpleHTTPRequestHandler):
	phenny = None

	def do_GET(self):
		parsed_params = urllib.parse.urlparse(self.path)
		query_parsed = urllib.parse.parse_qs(parsed_params.query)
		self.phenny.say("GET request on port %s: %s" % (PORT, str(query_parsed)))
		self.send_response(403)
		
	def do_POST(self):
		parsed_params = urllib.parse.urlparse(self.path)
		query_parsed = urllib.parse.parse_qs(parsed_params.query)
		
		try:
			payload = query_parsed['payload'][0]
		except KeyError:
			#self.phenny.say("Something went wrong with getting the data. WHAT.")
			#self.send_response(403)
			#return
		
		#data = json.loads(payload)
		self.phenny.say("GOT TEST DATA!!")
		self.phenny.say(str(query_parsed))
		
		self.send_response(200)
		
def setup_server(phenny):
	global Handler, httpd
	Handler = MyHandler
	Handler.phenny = phenny
	httpd = socketserver.TCPServer(("", PORT), Handler)
	phenny.say("Server is up and running on port %s" % PORT)
	httpd.serve_forever()

def github(phenny, input):
	global Handler
	if input.admin:
		if Handler is None:
			setup_server(phenny)
	else:
		phenny.reply("That is an admin-only command.")
github.name = 'startserver'
github.commands = ['startserver']
#github.event = 'JOIN'
#github.rule = r'.*'

def stopserver(phenny, input):
	global Handler, httpd
	if input.admin:
		httpd.shutdown()
		Handler = None
		httpd = None
		phenny.say("Server has stopped on port %s" % PORT)
	else:
		phenny.reply("That is an admin-only command.")
stopserver.commands = ['stopserver']