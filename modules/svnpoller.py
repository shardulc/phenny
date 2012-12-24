#!/usr/bin/env python
'''Push changes in subversion repository to IRC channel'''

from twisted.words.protocols import irc
from twisted.internet.protocol import ReconnectingClientFactory
import re
import os
from subprocess import Popen, PIPE
from xml.etree.cElementTree import parse as xmlparse
from cStringIO import StringIO

class IRCClient(irc.IRCClient):
    nickname = "begiak"
    realname = "begiak_bot"
    channel = "#apertium"

    instance = None # Running instance

    def signedOn(self):
        IRCClient.instance = self
        self.join(self.channel)

    def svn(self, revision, author, repo, dir, comment):
        if not comment:
            return
        comment = (comment[:77] + "...") if  len(comment) > 80 else comment
        message = "%s: %s * r%s: %s: %s" % (repo, author, revision, dir, comment.strip())
        self.say(self.channel, message)


class SVNPoller:
    def __init__(self, root):
        self.pre = ["svn", "--xml"]
        self.root = root
        self.repo = root.rpartition("/")[2]
        self.last_revision = self.get_last_revision()-1


    def check(self):
        if not IRCClient.instance:
            return

        try:
            last_revision = self.get_last_revision()
            if (not last_revision) or (last_revision == self.last_revision) or (last_revision == -1):
                return

            for rev in range(self.last_revision + 1, last_revision + 1):
                author, comment, dir = self.revision_info(rev)
                IRCClient.instance.svn(rev, author, self.repo, dir, comment)
            self.last_revision = last_revision
        except Exception, e:
#surpress all outputs...
            pass

    def svn(self, *cmd):
        pipe = Popen(self.pre +  list(cmd) + [self.root], stdout=PIPE)
        try:
            data = pipe.communicate()[0]
        except IOError:
            data = ""
        return xmlparse(StringIO(data))

    def get_last_revision(self):
        tree = self.svn("info")
        revision = tree.find("//commit").get("revision")
        return int(revision)

    def revision_info(self, revision):
        tree = self.svn("log", "-r", str(revision), "--verbose")
        author = tree.find("//author").text
        comment = tree.find("//msg").text
        dir = tree.find("//path").text

        return author, comment, dir


if __name__ == "__main__":

    from twisted.internet import reactor
    from twisted.internet.task import LoopingCall

    factory = ReconnectingClientFactory()
    factory.protocol = IRCClient
    reactor.connectTCP("irc.freenode.net", 6667, factory)

    toPolls = ["https://apertium.svn.sourceforge.net/svnroot/apertium",
        "https://hfst.svn.sourceforge.net/svnroot/hfst",
        "http://beta.visl.sdu.dk/svn/visl/tools/vislcg3"]

    for toPoll in toPolls
        poller = SVNPoller(toPoll)
        task = LoopingCall(poller.check)
        task.start(4)

    reactor.run()
