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
        nick        varchar(255)
    );''')

def greeting(phenny, input):
    if not greeting.conn:
        greeting.conn = sqlite3.connect(phenny.greeting_db)

    # Greeting Message
    try:
        nick = input.nick
    except UnboundLocalError:
        pass
    
    if nick.startswith("ap-vbox"):
        phenny.say(input.nick + ": I see that you have a default nickname enabled. You can change your nickname using: /nick <name>")
    
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

if __name__ == '__main__':
    print(__doc__.strip())
