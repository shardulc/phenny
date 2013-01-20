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
from tools import generate_report
import time

PORT = 1234

Handler = None
httpd = None

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
			self.phenny.bot.msg('#apertium', msg)
		
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
	if Handler is None and httpd is None:
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
#github.event = 'PRIVMSG'
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
	date = time.strptime(data['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
	date = time.strftime("%d %b %Y %H:%M:%S", date)
	return author, comment, modified_paths, added_paths, removed_paths, rev, date

def get_recent_commit(phenny, input):
	for repo in phenny.config.git_repositories:
		html = web.get(phenny.config.git_repositories[repo] + '/commits')
		data = json.loads(html)
		author, comment, modified_paths, added_paths, removed_paths, rev, date = get_commit_info(phenny, repo, data[0]['sha'])
		msg = generate_report(repo, author, comment, modified_paths, added_paths, removed_paths, rev, date)
		phenny.say(msg)
get_recent_commit.rule = ('$nick', 'recent')
get_recent_commit.priority = 'medium'
get_recent_commit.thread = True

def retrieve_commit(phenny, input):
	data = input.group(1).split(' ')
	
	if len(data) != 2:
		phenny.reply("Invalid number of parameters.")
		return
	
	repo = data[0]
	rev = data[1]
	
	if repo in phenny.config.svn_repositories:
		return
	
	if repo not in phenny.config.git_repositories:
		phenny.reply("That repository is not monitored by me!")
		return
	try:
		author, comment, modified_paths, added_paths, removed_paths, rev, date = get_commit_info(phenny, repo, rev)
	except:
		phenny.reply("Invalid revision value!")
		return
	msg = generate_report(repo, author, comment, modified_paths, added_paths, removed_paths, rev, date)
	phenny.say(msg)
retrieve_commit.rule = ('$nick', 'info(?: +(.*))')