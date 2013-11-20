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
	phInput = None
	
	def return_data(self, site, data, commit):
		#hrm, if I'm storing fields in a list in python, but I have something that has complex fields (e.g., data['foo']['bar']), is there some way to write a function that'll 
		#fields['github'] = ['phenny', data['pusher']['name'], commit['message'], commit['modified'], commit['added'], commit['removed'], commit['id'][:7]))
		if site=="github":
			name = "phenny"
			author = data['pusher']['name']
			message = commit['message']
			modified = commit['modified']
			added = commit['added']
			removed = commit['removed']
			rev = commit['id'][:7]
		elif site=="googlecode":
			name = data['project_name']
			author = commit['author']
			message = commit['message']
			modified = commit['modified']
			added = commit['added']
			removed = commit['removed']
			rev = commit['revision']
		elif site=="bitbucket":
			files = self.getBBFiles(commit['files'])
			name = 'turkiccorpora'
			author = commit['author']
			message = commit['message']
			modified = files['modified']
			added = files['added']
			removed = files['removed']
			rev = commit['node']
		return generate_report(name, author, message, modified, added, removed, rev)


	def do_GET(self):
		parsed_params = urllib.parse.urlparse(self.path)
		query_parsed = urllib.parse.parse_qs(parsed_params.query)
		#self.phenny.say("GET request on port %s: %s" % (PORT, str(query_parsed)))
		self.send_response(403)
		
	def do_POST(self):
		length = int(self.headers['Content-Length'])
		indata = self.rfile.read(length)
		#print("indata: "+str(indata))
		#print("headers: "+str(self.headers))
		post_data = urllib.parse.parse_qs(indata.decode('utf-8'))
		if len(post_data) == 0:
			post_data = indata.decode('utf-8')
		
		#try:
		#	payload = query_parsed['payload'][0]
		#except KeyError:
			#self.phenny.say("Something went wrong with getting the data. WHAT.")
			#self.send_response(403)
			#return
		#self.phenny.say(post_data['payload'][0])
		if "payload" in post_data:
			data = json.loads(post_data['payload'][0])
		else:
			#print(post_data)
			data = json.loads(post_data)
		#print(data)
		
		msgs = []
		if "commits" in data:
			for commit in data['commits']:
				try:
					if "committer" in commit:
					## For github
					#	msgs.append(generate_report('phenny', data['pusher']['name'], commit['message'], commit['modified'], commit['added'], commit['removed'], commit['id'][:7]))
						msgs.append(self.return_data("github", data, commit))
					#elif "pusher" in data:
					## for google code
					#	for commit in data['revisions']:
					#		msgs.append(self.return_data(self, "github", data, commit))
					#		#msgs.append()

					elif "author" in commit:
					## For bitbucket
						#msgs.append("unsupported data: "+str(commit))
						files = self.getBBFiles(commit['files'])
						msgs.append(generate_report('turkiccorpora', commit['author'], commit['message'], files['modified'], files['added'], files['removed'], commit['node']))
					else:
						msgs.append("unsupported data: "+str(commit))
				except Exception:
					#msgs.append("unsupported data: "+str(commit))
					print("unsupported data: "+str(commit))
		elif "project_name" in data:
			# for google code
			for commit in data['revisions']:
				msgs.append(self.return_data("googlecode", data, commit))
				#msgs.append()

		if len(msgs)==0:
			msgs = ["Something went wrong: "+str(data.keys())]
		for msg in msgs:
			for chan in self.phInput.chans:
				self.phenny.bot.msg(chan, msg)
		
		self.send_response(200)

	def getBBFiles(self, filelist):
		toReturn = {"added": [], "modified": [], "removed": []}
		for onefile in filelist:
			toReturn[onefile['type']].append(onefile['file'])
		return toReturn

def setup_server(phenny, input):
	global Handler, httpd
	Handler = MyHandler
	Handler.phenny = phenny
	Handler.phInput = input
	httpd = socketserver.TCPServer(("", PORT), Handler)
	phenny.say("Server is up and running on port %s" % PORT)
	httpd.serve_forever()

def github(phenny, input):
	global Handler, httpd
	if Handler is None and httpd is None:
		#if input.admin:
		if httpd is not None:
			httpd.shutdown()
			httpd = None
		if Handler is not None:
			Handler = None
		setup_server(phenny, input)
		#else:
		#	phenny.reply("That is an admin-only command.")
#github.name = 'startserver'
#github.commands = ['startserver']
##github.event = 'PRIVMSG'
##github.rule = r'.*'
github.name = 'start githook server'
github.event = "PONG"
github.rule = r'.*'
github.priority = 'medium'


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

def gitserver(phenny, input):
	''' control git server '''
	global Handler, httpd
	command = input.group(1).strip()
	if input.admin:
		if command=="stop":
			if httpd is not None:
				httpd.shutdown()
				httpd.socket.close()				
				httpd = None
			Handler = None
			phenny.say("Server has stopped on port %s" % PORT)
		if command=="start":
			if httpd is None:
				Handler = MyHandler
				Handler.phenny = phenny
				Handler.phInput = input
				httpd = socketserver.TCPServer(("", PORT), Handler)
				phenny.say("Server is up and running on port %s" % PORT)
				httpd.serve_forever()

	else:
		phenny.reply("Only admins control gitserver.")
gitserver.name = "gitserver"
gitserver.rule = ('.gitserver', '(.*)')

def gitserver_info(phenny, input):
	''' provides git server info '''
	global Handler, httpd
	command =  input.group(1).strip()
	if input.admin:
		if command=="stop":
			if httpd is not None:
				httpd.shutdown()
				httpd.socket.close()				
				httpd = None
			Handler = None
			phenny.say("Server has stopped on port %s" % PORT)
		if command=="start":
			if httpd is None:
				Handler = MyHandler
				Handler.phenny = phenny
				Handler.phInput = input
				httpd = socketserver.TCPServer(("", PORT), Handler)
				phenny.say("Server is up and running on port %s" % PORT)
				httpd.serve_forever()

	else:
		if httpd is None:	
			phenny.say("Server is down")
		else:	
			phenny.say("Server is up and running {only admins can shut it down}")
                
gitserver_info.name = "gitserver_info"
gitserver_info.rule = ('.gitserver_info', '(*)')

def get_commit_info(phenny, repo, sha):
	repoUrl = phenny.config.git_repositories[repo]
	#print(repoUrl)
	if repoUrl.find("code.google.com") >= 0:
		locationurl = '/source/detail?r=%s'
	elif repoUrl.find("api.github.com") >= 0:
		locationurl = '/commits/%s'
	elif repoUrl.find("bitbucket.org") >=0:
		locationurl = ''
	#print(locationurl)
	html = web.get(repoUrl + locationurl % sha)
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
