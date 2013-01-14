#!/usr/bin/env python
"""
github.py - Github Post-Receive Hooks Module
"""

import http.server
import socketserver
import urllib.parse
import json
import re
import os
import web
from io import StringIO

PORT = 1234

Handler = None
httpd = None

def generate_report(repo, author, comment, modified_paths, added_paths, removed_paths, rev):
	paths = modified_paths + added_paths + removed_paths

	if comment is None:
		comment = "Use comments people -_-"
	else:
		comment = re.sub("[\n\r]+", " ␍ ", comment.strip())
		
	basepath = os.path.commonprefix(paths)
	if basepath[-1] != "/":
		basepath = basepath.split("/")
		basepath.pop()
		basepath = '/'.join(basepath) + "/"
		
	textPaths = ""
	count = 0
	first = False
	if len(paths) > 0:
		for path in paths:
			if count != 0 and first == False:
				textPaths += ", "
			count += 1
			if count < 4:
				textPaths += os.path.relpath(path, basepath)
				if path in added_paths:
					textPaths += " (+)"
				elif path in removed_paths:
					textPaths += " (-)"
			elif count >= 4 and first == False:
				textPaths = textPaths.split(", ")
				textPaths.pop()
				textPaths = ', '.join(textPaths)
				textPaths+="%sand %s other files" % " ", (str(len(paths) - 3))
				first = True
		if len(paths) > 1:
			finalPath = "%s: %s" % (basepath, textPaths)
		else:
			finalPath = paths[0]
			if path in added_paths:
				finalPath += " (+)"
			elif path in removed_paths:
				finalPath += " (-)"
		msg = "%s: %s * %s: %s: %s" % (repo, author, rev, finalPath, comment.strip())
	return msg
	
class MyHandler(http.server.SimpleHTTPRequestHandler):
	phenny = None
	
	def do_GET(self):
		parsed_params = urllib.parse.urlparse(self.path)
		query_parsed = urllib.parse.parse_qs(parsed_params.query)
		#self.phenny.say("GET request on port %s: %s" % (PORT, str(query_parsed)))
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
		#self.phenny.say(post_data['payload'][0])
		data = json.loads(post_data['payload'][0])
		
		msgs = []
		for commit in data['commits']:
			msgs.append(generate_report('phenny', data['pusher']['name'], commit['message'], commit['modified'], commit['added'], commit['removed'], commit['id'][:7]))
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
	global Handler, httpd
	if input.admin:
		if httpd is not None:
			httpd.shutdown()
			httpd = None
		if Handler is not None:
			Handler = None
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
		if httpd is not None:
			httpd.shutdown()
			httpd = None
		Handler = None
		phenny.say("Server has stopped on port %s" % PORT)
	else:
		phenny.reply("That is an admin-only command.")
stopserver.commands = ['stopserver']

def get_commit_info(phenny, repo, sha):
	html = web.get(phenny.config.git_repositories[repo] + '/commits/%s' % sha)
	data = json.loads(html)
	author = data['commit']['committer']['name']
	comment = data['commit']['message']
	
	modified_paths = []
	added_paths = []
	removed_paths = []
	
	for file in data['files']:
		if file['status'] == 'modified':
			modified_paths.append(file['filename'])
		elif file['status'] == 'added':
			added_paths.append(file['filename'])
		elif file['status'] == 'removed':
			removed_paths.append(file['filename'])
	rev = sha[:7]
	return author, comment, modified_paths, added_paths, removed_paths, rev

def get_recent_commit(phenny, input):
	for repo in phenny.config.git_repositories:
		html = web.get(phenny.config.git_repositories[repo] + '/commits')
		data = json.loads(html)
		author, comment, modified_paths, added_paths, removed_paths, rev = get_commit_info(phenny, repo, data[0]['sha'])
		msg = generate_report(repo, author, comment, modified_paths, added_paths, removed_paths, rev)
		phenny.say(msg)
get_recent_commit.rule = ('$nick', 'recent')
get_recent_commit.priority = 'medium'
get_recent_commit.thread = True