#!/usr/bin/env python3
"""
bot.py - Phenny IRC Bot
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import importlib
import irc
import logging
import os
import re
import sys
import threading
import traceback
import tools

logger = logging.getLogger('phenny')

home = os.getcwd()

def decode(bytes): 
    if type(bytes) == str:
        return bytes
    try:
        text = bytes.decode('utf-8')
    except UnicodeDecodeError: 
        try:
            text = bytes.decode('iso-8859-1')
        except UnicodeDecodeError: 
            text = bytes.decode('cp1252')
    except AttributeError:
        return bytes
    return text

class Phenny(irc.Bot): 
    def __init__(self, config): 
        args = (config.nick, config.name, config.channels, config.password)
        irc.Bot.__init__(self, *args)
        self.config = config
        self.doc = {}
        self.stats = {}
        self.setup()

    def setup(self): 
        self.variables = {}

        filenames = []
        if not hasattr(self.config, 'enable'): 
            for fn in os.listdir(os.path.join(home, 'modules')): 
                if fn.endswith('.py') and not fn.startswith('_'): 
                    filenames.append(os.path.join(home, 'modules', fn))
        else: 
            for fn in self.config.enable: 
                filenames.append(os.path.join(home, 'modules', fn + '.py'))

        if hasattr(self.config, 'extra'): 
            for fn in self.config.extra: 
                if os.path.isfile(fn): 
                    filenames.append(fn)
                elif os.path.isdir(fn): 
                    for n in os.listdir(fn): 
                        if n.endswith('.py') and not n.startswith('_'): 
                            filenames.append(os.path.join(fn, n))

        tools.setup(self)

        modules = []
        excluded_modules = getattr(self.config, 'exclude', [])
        for filename in filenames: 
            name = os.path.basename(filename)[:-3]
            if name in excluded_modules: continue
            # if name in sys.modules: 
            #     del sys.modules[name]
            try:
                module_loader = importlib.machinery.SourceFileLoader(name, filename)
                module = module_loader.load_module()

                if hasattr(module, 'setup'):
                    module.setup(self)
            except Exception as e: 
                trace = traceback.format_exc()
                logger.error("Error loading %s module:\n%s" % (name, trace))
            else: 
                self.register(module)
                modules.append(name)

        if modules: 
            logger.info('Registered modules: ' + ', '.join(modules))
        else:
            logger.warning("Couldn't find any modules")

        self.bind_commands()

    def register(self, module):
        # This is used by reload.py, hence it being methodised
        if module.__name__ not in self.variables:
            self.variables[module.__name__] = {}

        for name, obj in vars(module).items():
            if hasattr(obj, 'commands') or hasattr(obj, 'rule'): 
                self.variables[module.__name__][name] = obj

    def bind(self, module, name, func, regexp):
        # register documentation
        if not hasattr(func, 'name'):
            func.name = func.__name__

        if func.__doc__:
            if hasattr(func, 'example'):
                example = func.example
                example = example.replace('$nickname', self.nick)
            else: example = None

            self.doc[func.name] = (func.__doc__, example)

        self.commands[func.priority].setdefault(regexp, []).append(func)

    def bind_command(self, module, name, func):
        logger.debug("Binding module '{:}' command '{:}'".format(module, name))

        if not hasattr(func, 'priority'):
            func.priority = 'medium'

        if not hasattr(func, 'thread'):
            func.thread = True

        if not hasattr(func, 'event'):
            func.event = 'PRIVMSG'
        else:
            func.event = func.event.upper()

        def sub(pattern, self=self): 
            # These replacements have significant order
            pattern = pattern.replace('$nickname', re.escape(self.nick))
            return pattern.replace('$nick', r'%s[,:] +' % re.escape(self.nick))

        if hasattr(func, 'rule'):
            if isinstance(func.rule, str):
                pattern = sub(func.rule)
                regexp = re.compile(pattern)
                self.bind(module, name, func, regexp)

            if isinstance(func.rule, tuple):
                # 1) e.g. ('$nick', '(.*)')
                if len(func.rule) == 2 and isinstance(func.rule[0], str):
                    prefix, pattern = func.rule
                    prefix = sub(prefix)
                    regexp = re.compile(prefix + pattern)
                    self.bind(module, name, func, regexp)

                # 2) e.g. (['p', 'q'], '(.*)')
                elif len(func.rule) == 2 and isinstance(func.rule[0], list):
                    prefix = self.config.prefix
                    commands, pattern = func.rule
                    for command in commands:
                        command = r'(%s)\b(?: +(?:%s))?' % (command, pattern)
                        regexp = re.compile(prefix + command)
                        self.bind(module, name, func, regexp)

                # 3) e.g. ('$nick', ['p', 'q'], '(.*)')
                elif len(func.rule) == 3:
                    prefix, commands, pattern = func.rule
                    prefix = sub(prefix)
                    for command in commands:
                        command = r'(%s) +' % command
                        regexp = re.compile(prefix + command + pattern)
                        self.bind(module, name, func, regexp)

        if hasattr(func, 'commands'):
            for command in func.commands:
                template = r'^%s(%s)(?: +(.*))?$'
                pattern = template % (self.config.prefix, command)
                regexp = re.compile(pattern)
                self.bind(module, name, func, regexp)

    def bind_commands(self):
        self.commands = {'high': {}, 'medium': {}, 'low': {}}

        for module, functions in self.variables.items():
            for name, func in functions.items():
                self.bind_command(module, name, func)

    def wrapped(self, origin, text, match): 
        class PhennyWrapper(object): 
            def __init__(self, phenny): 
                self.bot = phenny

            def __getattr__(self, attr): 
                sender = origin.sender or text
                if attr == 'reply': 
                    return (lambda msg: 
                        self.bot.msg(sender, origin.nick + ': ' + msg))
                elif attr == 'say': 
                    return lambda msg: self.bot.msg(sender, msg)
                elif attr == 'do':
                    return lambda msg: self.bot.action(sender, msg)
                return getattr(self.bot, attr)

        return PhennyWrapper(self)

    def input(self, origin, text, bytes, match, event, args):
        class CommandInput(str): 
            def __new__(cls, text, origin, bytes, match, event, args): 
                s = str.__new__(cls, text)
                s.sender = decode(origin.sender)
                s.nick = decode(origin.nick)
                s.event = event
                s.bytes = bytes
                s.match = match
                s.group = match.group
                s.groups = match.groups
                s.args = args
                s.admin = s.nick in self.config.admins
                s.owner = s.nick == self.config.owner
                s.chans = self.config.channels
                #s.bot = self.bot
                return s

        return CommandInput(text, origin, bytes, match, event, args)

    def call(self, func, origin, phenny, input): 
        try: func(phenny, input)
        except tools.GrumbleError as e:
            self.msg(origin.sender, str(e))
        except Exception as e: 
            self.error(origin)

    def limit(self, origin, func): 
        if origin.sender and origin.sender.startswith('#'): 
            if hasattr(self.config, 'limit'): 
                limits = self.config.limit.get(origin.sender)
                if limits and (func.__module__ not in limits): 
                    return True
        return False

    def dispatch(self, origin, args): 
        bytes, event = args[0], args[1]
        text = decode(bytes)
        event = decode(event)

        if origin.nick in self.config.ignore:
             return

        for priority in ('high', 'medium', 'low'): 
            items = list(self.commands[priority].items())
            for regexp, funcs in items: 
                for func in funcs: 
                    if event != func.event and func.event != '*': continue

                    match = regexp.match(text)
                    if match: 
                        if self.limit(origin, func): continue

                        phenny = self.wrapped(origin, text, match)
                        input = self.input(origin, text, bytes, match, event, args)

                        if func.thread: 
                            targs = (func, origin, phenny, input)
                            t = threading.Thread(target=self.call, args=targs, name=func.name)
                            t.start()
                        else: self.call(func, origin, phenny, input)

                        for source in [decode(origin.sender), decode(origin.nick)]: 
                            try: self.stats[(func.name, source)] += 1
                            except KeyError: 
                                self.stats[(func.name, source)] = 1

if __name__ == '__main__': 
    print(__doc__)
