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

def generateReport(data):
	msgs = []
	for commit in data['commits']:
		author = commit['author']['name']
		comment = commit['message']
		paths = commit['modified']
		if comment is None:
			comment = "Use comments people -_-"
		else:
			comment = re.sub("[\n\r]+", " ␍ ", comment.strip())
		basepath = os.path.commonprefix(paths)
		textPaths = ""
		count = 0
		first = False
		for path in paths:
			if count != 0 and first == False:
				textPaths+=", "
			count += 1
			if count < 3:
				textPaths+=os.path.relpath(path, basepath)
			elif count >= 3 and first == False:
				if (len(paths) - 2) > 1:
					plural = "s"
				else:
					plural = ""
				textPaths+="and %s other file%s" % (str(len(paths) - 2), plural)
				first = True
		if len(paths) > 1:
			finalPath = "%s: %s" % (basepath, textPaths)
		else:
			finalPath = paths[0]
		msg = "%s: %s * r%s: %s: %s\n" % (data['repository']['name'], author, '0000', finalPath, comment.strip())
		msgs.append(msg)
	return msgs

class MyHandler(http.server.SimpleHTTPRequestHandler):
	phenny = None

	def do_GET(self):
		parsed_params = urllib.parse.urlparse(self.path)
		query_parsed = urllib.parse.parse_qs(parsed_params.query)
		self.phenny.say("GET request on port %s: %s" % (PORT, str(query_parsed)))
		self.send_response(403)
		
	def do_POST(self):
		length = int(self.headers['Content-Length'])
		post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
		
		#try:
		#	payload = query_parsed['payload'][0]
		#except KeyError:
			#self.phenny.say("Something went wrong with getting the data. WHAT.")
			#self.send_response(403)
			#return
		
		data = json.loads(post_data['payload'][0])
		msgs = generateReport(data)
		for msg in msgs:
			self.phenny.say(msg)
		
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