#!/usr/bin/env python
'''A Phenny extension that polls SVN repos'''

import re
import os
from subprocess import Popen, PIPE
from xml.etree.ElementTree import parse as xmlparse
from io import StringIO

Repos = {"apertium": "https://apertium.svn.sourceforge.net/svnroot/apertium",
	"hfst": "https://hfst.svn.sourceforge.net/svnroot/hfst",
	"vislcg3": "http://beta.visl.sdu.dk/svn/visl/tools/vislcg3"}

def loadRevisions(fn): 
	result = {}
	with open(fn) as f:
		for line in f: 
			line = line.strip()
			if line: 
				try: repo, rev = line.split('\t', 2)
				except ValueError: continue # @@ hmm
				result.setdefault(repo, rev) #[]).append((teller, verb, timenow, msg))
	return result

def dumpRevisions(fn, data): 
	with open(fn, 'w') as f:
		for repo in data.keys():
			line = '\t'.join((repo, str(data[repo])))
			try: f.write(line + '\n')
			except IOError: break
	return True

def setup(self): 
	fn = self.nick + '-' + self.config.host + '.repos.db'
	self.repos_filename = os.path.join(os.path.expanduser('~/.phenny'), fn)
	if not os.path.exists(self.repos_filename): 
		try: f = open(self.repos_filename, 'w')
		except OSError: pass
		else: 
			f.write('')
			f.close()
	self.revisions = loadRevisions(self.repos_filename) # @@ tell



class SVNPoller:
	def __init__(self, repo, root):
		self.pre = ["svn", "--xml"]
		self.root = root
		#self.repo = root.rpartition("/")[2]
		self.repo = repo

		#if os.path.exists("svn_data/"+self.repo+"_current_rev"):
		#	self.last_revision = int(open("svn_data/"+self.repo+"_current_rev").read())
		#	print((str(self.last_revision)+" gotten from file."))
		#else:
		#	self.last_revision = self.get_last_revision()
		#	repo_file = open("svn_data/"+self.repo+"_current_rev", 'w')
		#	repo_file.write(str(self.last_revision))
		#	repo_file.close()
		#	print((str(self.last_revision)+" gotten from self.get_last_revision()"))
		self.last_revision = None

	def __str__(self):
		return "(%s) %s %s" % (self.repo, self.root, self.last_revision)

	def check(self, revisions):
		#try:
		#	self.last_revision = revisions[self.repo]
		#	phenny.say(str(self.last_revision))
		#	last_revision = self.get_last_revision()
		#	phenny.say(str(last_revision))
		#	last_revision = self.get_last_revision()
		#	if (not last_revision) or (last_revision == self.last_revision) or (last_revision == -1):
		#		return revisions
		#
		#	for rev in range(self.last_revision + 1, last_revision + 1):
		#		author, comment, dir = self.revision_info(rev)
		#		if comment is None:
		#			comment = "Use comments people -_-"
		#		#outfile = open("svn_data/"+self.repo+"_output", 'w')
		#		#outfile.write("%s: %s * r%s: %s: %s\n" % (self.repo, author, rev, dir, comment.strip()))
		#		#outfile.close()
		#
		#	self.last_revision = last_revision
		#	revisions[self.repo] = self.last_revision
		#	
		#	#repo_file = open("svn_data/"+self.repo+"_current_rev", 'w')
		#	#repo_file.write(str(self.last_revision))
		#	#repo_file.close()
		#	print("REPO UPDATE: "+self.repo+" -> "+str(self.last_revision))
		#	return revisions
		#
		#except Exception as e:
		#	print(("check: ERROR: %s" % e))
		#	return
		if self.repo not in revisions:
			revisions[self.repo] = 0
		self.revisions = revisions
		self.last_revision = self.revisions[self.repo]
		last_revision = self.get_last_revision()
		print(str(last_revision), str(self.last_revision), str(self.revisions))
		## if successfully polled and a new revision ##
		if last_revision > self.last_revision:
			for msg in self.newReport(last_revision):
				yield (msg, self.revisions)
		## if nothing set yet ##
		## if changed ##
		#if self.last_revision == 0 or self.last_revision == None:
		#	print(str(self.last_revision))
		#	for msg in self.newReport(0):
		#		yield (msg, self.revisions)
		#elif (last_revision > self.last_revision):
		#	print(str(self.last_revision))
		#	for msg in self.newReport(self.last_revision):
		#		yield (msg, self.revisions)
		#else:
		#	print(str(last_revision), str(self.last_revision))

	def newReport(self, last_revision):
		if self.last_revision == 0 or self.last_revision == None:
			self.last_revision = last_revision -1
		print("newReport", str(last_revision), str(self.last_revision))

		for rev in range(self.last_revision+1, last_revision+1):
			author, comment, dir = self.revision_info(rev)
			if comment is None:
				comment = "Use comments people -_-"
			msg = "%s: %s * r%s: %s: %s\n" % (self.repo, author, rev, dir, comment.strip())
		if not msg:
			msg = ":("
		yield msg


	def svn(self, *cmd):
		command = " ".join(self.pre)
		command = command + " " + " ".join(list(cmd))
		command = command + " " + " ".join([self.root])
		pipe = Popen(command.split(" "), stdout=PIPE)
		try:
			data = pipe.communicate()[0]
		except IOError:
			data = ""
		return xmlparse(StringIO(data.decode()))


	def get_last_revision(self):
		tree = self.svn("info")
		revision = tree.find("//commit").get("revision")
		#phenny.say(str(revision))
		self.revisions[self.repo] = int(revision)
		return int(revision)


	def revision_info(self, revision):
		tree = self.svn("log", "-r", str(revision), "--verbose")
		author = tree.find("//author").text
		comment = tree.find("//msg").text
		dir = tree.find("//path").text

		return author, comment, dir

def pollsvn(phenny, input):
	print("POLLING!!!!")
	pollers = {}
	for repo in Repos:
		pollers[repo] = SVNPoller(repo, Repos[repo])
	for repo in Repos:
		for (msg, revisions) in pollers[repo].check(phenny.revisions):
			if phenny.revisions:
				if revisions[repo] != phenny.revisions[repo]:
					phenny.revisions = revisions
					phenny.say("New revisions!"+msg)
				else:
					phenny.say("No new revisions!")
				print(repo, str(phenny.revisions))
			else:
				phenny.say("First revisions!")
				phenny.revisions = revisions
			phenny.say("rev data: "+str(pollers[repo]))
			if phenny.revisions:
				if len(phenny.revisions)>0:
					dumpRevisions(phenny.repos_filename, phenny.revisions)
		
		
	#poller1 = SVNPoller("https://apertium.svn.sourceforge.net/svnroot/apertium")
	#poller2 = SVNPoller("https://hfst.svn.sourceforge.net/svnroot/hfst")
	#poller3 = SVNPoller("http://beta.visl.sdu.dk/svn/visl/tools/vislcg3")
	#
	#poller1_return = poller1.check()
	#poller2_return = poller2.check()
	#poller3_return = poller3.check()

	print("POLLED")

pollsvn.name = 'SVN poll'
#pollsvn.rule = ('$nick', ['esan!'], r'(\S+)?')
pollsvn.rule = ('$nick', ['esan!'], '')
pollsvn.priority = 'medium'
#pollsvn.thread = True

