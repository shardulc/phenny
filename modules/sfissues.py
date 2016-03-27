import time
import os
import shelve
import feedparser
import threading

db = None


def queue_poll(phenny, secs):
    phenny.sf_issues_timer = threading.Timer(secs, poll_sf_issues, (phenny,))
    phenny.sf_issues_timer.start()


def setup(phenny):
    global db
    if not hasattr(phenny.config, 'sf_issues'):
        print("Sourceforge issues not configured, aborting.")
        return
    db_fn = os.path.expanduser('~/.phenny/sfissues.db')
    db = shelve.open(db_fn)
    for proj, url in phenny.config.sf_issues.items():
        if proj not in db:
            db[proj] = time.time() - 3 * 24 * 60 * 60
    queue_poll(phenny, 30)


def poll_sf_issues(phenny):
    were_results = False
    for proj, (url, chans) in phenny.config.sf_issues.items():
        feed = feedparser.parse(url)
        latest = db[proj]
        for entry in reversed(feed.entries):
            for chan in chans:
                pub_time = time.mktime(entry.published_parsed)
                if pub_time > db[proj]:
                    were_results = True
                    if '?' in entry.link:
                        type = 'Comment on'
                    elif '<strong>status</strong>' in entry.description:
                        type = 'Status change on'
                    else:
                        type = 'New ticket:'

                    msg = "{} bugs: {} {} {}".format(
                            proj, type, entry.title, entry.link)
                    phenny.msg(chan, msg)
                    if pub_time > latest:
                        latest = pub_time
        db[proj] = latest
    queue_poll(phenny, 5 * 60)
    return were_results


def bugs(phenny, input):
    phenny.reply("Hold on a second, I'm polling!")
    results = poll_sf_issues(phenny, input)
    if not results:
        phenny.reply("Sorry, there was nothing to report.")
bugs.rule = ('$nick', 'bugs!')
