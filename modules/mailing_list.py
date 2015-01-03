"""
mailing_list.py - mailing list reporter
author: mattr555 <mattramina@gmail.com>
"""
import threading
import imaplib
import email
import re

def setup(phenny):
    phenny.mailing_list_timer = threading.Timer(60*5, check_mail, (phenny,))
    phenny.mailing_list_timer.start()

def recipients(e):
    return e.get('From', '') + e.get('To', '') + e.get('CC', '')

def get_text(e):
    maintype = e.get_content_maintype()
    if maintype == "multipart":
        for part in e.get_payload():
            if part.get_content_maintype() == "text":
                return part.get_payload()
    elif maintype == "text":
        return e.get_payload()

def strip_reply_lines(e):
    message = get_text(e).split('\n')
    stripped = []
    for i in message:
        if i.startswith('>'):
            continue
        stripped.append(i)
    return " ␍ ".join(stripped)

def check_mail(phenny):
    found = False
    try:
        mail = imaplib.IMAP4_SSL(phenny.config.imap_server)
        mail.login(phenny.config.imap_user, phenny.config.imap_pass)
    except imaplib.error:
        phenny.say('IMAP connection/auth failed :(')
        return found
    mail.select('inbox')
    rc, data = mail.uid('search', None, 'UNSEEN')
    unseen_mails = data[0].split()
    print(unseen_mails)

    for uid in unseen_mails:
        rc, data = mail.uid('fetch', uid, '(RFC822)')
        e = email.message_from_string(data[0][1].decode('utf8'))
        for name, (address, channel) in phenny.config.mailing_lists.items():
            if address in recipients(e):
                found = True
                message = '{} on "{}" in {}: {}'.format(e['From'], e['Subject'], name, strip_reply_lines(e))
                if len(message) > 200:
                    phenny.msg(channel, message[:195] + '[...]')
                else:
                    phenny.msg(channel, message)
        rc, data = mail.uid('store', uid, '+FLAGS', '(\\Seen)')

    mail.logout()
    phenny.mailing_list_timer = threading.Timer(60*5, check_mail, (phenny,))
    phenny.mailing_list_timer.start()
    return found

def list_report(phenny, input):
    ".mailinglist - poll for new mailing list messages"
    phenny.reply('Ok, polling.')
    if not check_mail(phenny):
        phenny.reply('Sorry, no unread mailing list messages.')
list_report.name = "mailing list reporter"
list_report.rule = ('.mailinglist')
list_report.priority = 'medium'
list_report.thread = True
