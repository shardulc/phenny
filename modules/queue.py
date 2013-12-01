"""
.queue - list management
author: mattr555
"""

import os
import pickle

commands = '.queue display, .queue new, .queue delete, .queue <name> add, .queue <name> swap, .queue <name> remove'

def filename(phenny):
    name = phenny.nick + '-' + phenny.config.host + '.queue.db'
    return os.path.join(os.path.expanduser('~/.phenny'), name)

def write_dict(filename, data):
    with open(filename, 'wb') as f:
        f.write(pickle.dumps(data))

def read_dict(filename):
    data = None
    with open(filename, 'rb') as f:
        data = pickle.loads(f.read())
    return data

def setup(phenny):
    f = filename(phenny)
    if os.path.exists(f):
        phenny.queue_data = read_dict(f)
    else:
        phenny.queue_data = {}

def search_queue(queue, query):
    for i in range(len(queue)):
        if query.lower() in queue[i].lower():
            index = int(i)
            break
    return index

def print_queue(queue_name, queue):
    return '[{}] (by {}): {}'.format(
        queue_name, queue['owner'], ', '.join(queue['queue']) if queue['queue'] else '<empty>')

def queue(phenny, raw):
    """.queue- queue management."""
    if raw.group(1):
        command = raw.group(1)
        if command.lower() == 'display':
            queue_name = raw.group(2)
            if queue_name in phenny.queue_data:
                queue = phenny.queue_data[queue_name]
                phenny.reply(print_queue(queue_name, queue))
            else:
                phenny.reply('That queue wasn\'t found.')

        elif command.lower() == 'new':
            if raw.group(2):
                queue_name = raw.group(2)
                owner = raw.nick
                if raw.group(3):
                    queue = raw.group(3).split(',')
                    queue = list(map(lambda x: x.strip(), queue))
                    phenny.queue_data[queue_name] = {'owner': owner, 'queue': queue}
                    write_dict(filename(phenny), phenny.queue_data)
                    phenny.reply('Queue {} with items {} created.'.format(
                        queue_name, ', '.join(queue)))
                else:
                    phenny.queue_data[queue_name] = {'owner': owner, 'queue': []}
                    write_dict(filename(phenny), phenny.queue_data)
                    phenny.reply('Empty queue {} created.'.format(queue_name))
            else:
                phenny.reply('Syntax: .queue new <name> <item1>, <item2> ...')

        elif command.lower() == 'delete':
            if raw.group(2):
                queue_name = raw.group(2)
                if raw.nick == phenny.queue_data[queue_name]['owner'] or raw.admin:
                    phenny.queue_data.pop(queue_name)
                    write_dict(filename(phenny), phenny.queue_data)
                    phenny.reply('Queue {} deleted.'.format(queue_name))
                else:
                    phenny.reply('You aren\'t authorized to do that!')
            else:
                phenny.reply('Syntax: .queue delete <name>')

        elif command in phenny.queue_data:
            #queue-specific commands
            queue_name = raw.group(1)
            queue = phenny.queue_data[queue_name]
            if raw.group(2):
                command = raw.group(2).lower()
                if queue['owner'] == raw.nick:
                    if command == 'add':
                        if raw.group(3):
                            new_queue = raw.group(3).split(',')
                            new_queue = list(map(lambda x: x.strip(), new_queue))
                            queue['queue'] += new_queue
                            write_dict(filename(phenny), phenny.queue_data)
                            phenny.reply(print_queue(queue_name, queue))
                        else:
                            phenny.reply('Syntax: .queue <name> add <item1>, <item2> ...')
                    elif command == 'swap':
                        if raw.group(3):
                            indices = raw.group(3).split(',')
                            try:
                                id1, id2 = tuple(map(lambda x: int(x.strip()), indices))[:2]
                            except ValueError:
                                q1, q2 = tuple(map(lambda x: x.strip(), indices))[:2]
                                id1 = search_queue(queue['queue'], q1)
                                if id1 is None:
                                    phenny.reply('{} not found in {}'.format(indices[0].strip(), queue_name))
                                    return
                                id2 = search_queue(queue['queue'], q2)
                                if id2 is None:
                                    phenny.reply('{} not found in {}'.format(indices[1].strip(), queue_name))
                                    return
                            queue['queue'][id1], queue['queue'][id2] = queue['queue'][id2], queue['queue'][id1]
                            write_dict(filename(phenny), phenny.queue_data)
                            phenny.reply(print_queue(queue_name, queue))
                        else:
                            phenny.reply('Syntax: .queue <name> swap <index/item1>, <index/item2>')
                    elif command == 'remove':
                        if raw.group(3):
                            item = raw.group(3)
                            if item in queue['queue']:
                                queue['queue'].remove(item)
                                write_dict(filename(phenny), phenny.queue_data)
                                phenny.reply(print_queue(queue_name, queue))
                            elif search_queue(queue['queue'], item):
                                queue['queue'].pop(search_queue(queue['queue'], item))
                                write_dict(filename(phenny), phenny.queue_data)
                                phenny.reply(print_queue(queue_name, queue))
                            else:
                                phenny.reply('{} not found in {}'.format(item, queue_name))
                        else:
                            phenny.reply('Syntax: .queue <name> remove <item>')
                else:
                    phenny.reply('You aren\'t the owner of this queue!')
            else:
                phenny.reply(print_queue(queue_name, queue))
        else:
            if raw.group(3):
                phenny.reply('That\'s not a command. Commands: ' + commands)
            else:
                phenny.reply('That queue wasn\'t found!')
    else:
        phenny.reply('Commands: ' + commands)

queue.rule = r'\.queue(?:\s(\w+))?(?:\s(\w+))?(?:\s(.*))?'
