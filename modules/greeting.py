#!/usr/bin/python3
import os
import sqlite3

def setup(self):
    fn = self.nick + '-' + self.config.host + '.greeting.db'
    self.greeting_db = os.path.join(os.path.expanduser('~/.phenny'), fn)
    self.greeting_conn = sqlite3.connect(self.greeting_db)

    c = self.greeting_conn.cursor()
    c.execute('''create table if not exists lines_by_nick (
        channel     varchar(255),
        nick        varchar(255),
        unique (channel, nick) on conflict replace
    );''')
    c.execute('''create table if not exists special_nicks (
        message     varchar(255),
        nick        varchar(255),
        channel     varchar(255),
        unique (channel, nick) on conflict replace
    );''')
    c.close()

def greeting(phenny, input):
    if not greeting.conn:
        greeting.conn = sqlite3.connect(phenny.greeting_db)

    # Greeting Message
    try:
        nick = input.nick
    except UnboundLocalError:
        pass
    
    c = greeting.conn.cursor()
    c.execute("SELECT * FROM special_nicks WHERE nick = ? AND channel = ?", (nick.lower(), input.sender))
    try:
        phenny.say(input.nick + ": " + str(c.fetchone()[0]))
    except TypeError:
        pass
    c.close()
    
    c = greeting.conn.cursor()
    c.execute("SELECT * FROM lines_by_nick WHERE nick = ?", (nick.lower(),))
    if c.fetchone() == None:
        phenny.say(input.nick + ": Welcome to " + input.sender + ", " + input.nick + "! Please stick around for a while and someone will address any questions you have.")
    c.close()
    
    sqlite_data = {
        'channel': input.sender,
        'nick': input.nick.lower(),
     }
        
    c = greeting.conn.cursor()
    c.execute('''insert or replace into lines_by_nick
                    (channel, nick)
                    values(
                        :channel,
                        :nick
                    );''', sqlite_data)
    c.close()
    greeting.conn.commit()
    
greeting.conn = None
greeting.event = "JOIN"
greeting.priority = 'low'
greeting.rule = r'(.*)'
greeting.thread = False

def greeting_add(phenny, input):
    if input.admin:
        if input.group(2) == None:
            phenny.reply ("You haven't specified a name and message.")
            return
        elif len(input.group(2).split(" ")) < 2:
            phenny.reply ("You haven't specified a message.")
            return
        
        sqlite_data = {
            'channel': input.sender,
            'nick': input.group(2).split(" ")[0].lower(),
            'message': input.group(2).split(" ", 1)[1]
        }
        
        dbconnection = sqlite3.connect(phenny.greeting_db)
        c = dbconnection.cursor()
        c.execute('''insert or replace into special_nicks
                    (channel, nick, message)
                    values(
                        :channel,
                        :nick,
                        :message
                    );''', sqlite_data)
        c.close()
        
        c = dbconnection.cursor()
        c.execute('update special_nicks set message=:message where channel=:channel \
                    and nick=:nick', sqlite_data)
        c.close()
        
        dbconnection.commit()
        
        phenny.reply("Successfully added " + input.group(2).split(" ", 1)[0] + " to the special greetings list.")
    else:
        phenny.reply("You have insufficient privelleges to use this command.")
    
greeting_add.rule = (['greeting add'], r'(.*)')
greeting_add.name = 'greeting add'
greeting.priority = 'low'

def greeting_del(phenny, input):
    if input.admin:
        if input.group(2) == None:
            phenny.reply ("You haven't specified a name.")
            return
        
        dbconnection = sqlite3.connect(phenny.greeting_db)
        c = dbconnection.cursor()
        c.execute("DELETE FROM special_nicks WHERE nick = ? AND channel = ?", (input.group(2).split(" ")[0].lower(), input.sender))
        c.close()
        dbconnection.commit()
        
        phenny.reply("Successfully deleted " + input.group(2).split(" ", 1)[0] + " from the special greetings list.")
    else:
        phenny.reply("You have insufficient privelleges to use this command.")
greeting_del.rule = (['greeting del'], r'(.*)')
greeting_del.name = 'greeting del'
greeting.priority = 'low'
    

if __name__ == '__main__':
    print(__doc__.strip())
