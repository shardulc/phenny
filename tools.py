#!/usr/bin/env python3
"""
tools.py - Phenny Tools
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import os

class GrumbleError(Exception):
    pass


def deprecated(old): 
    def new(phenny, input, old=old): 
        self = phenny
        origin = type('Origin', (object,), {
            'sender': input.sender, 
            'nick': input.nick
        })()
        match = input.match
        args = [input.bytes, input.sender, '@@']

        old(self, origin, match, args)
    new.__module__ = old.__module__
    new.__name__ = old.__name__
    return new

def generate_report(repo, author, comment, modified_paths, added_paths, removed_paths, rev, date=""):
    paths = modified_paths + added_paths + removed_paths
    if comment is None:
        comment = "No commit message provided!"
    else:
        comment = re.sub("[\n\r]+", " ␍ ", comment.strip())
    
    basepath = os.path.commonprefix(paths)
    if basepath[-1] != "/":
        basepath = basepath.split("/")
        basepath.pop()
        basepath = '/'.join(basepath) + "/"
        
    text_paths = []
    if len(paths) > 0:
        for path in paths:
            addition = ""
            if path in added_paths:
                addition = " (+)"
            elif path in removed_paths:
                addition = " (-)"
            text_paths.append(os.path.relpath(path, basepath) + addition)
        if len(text_paths) > 1:
            if len(text_paths) <= 3: 
                final_path = "%s: %s" % (basepath, ', '.join(text_paths))
            else:
                final_path = "%s: %s" % (basepath, ', '.join([text_paths[0], text_paths[1]]) + ' and %s other files' % str(len(text_paths) - 2))
        else:
            final_path = paths[0]
            if final_path in added_paths:
                final_path += " (+)"
            elif final_path in removed_paths:
                final_path += " (-)"
    if date == "":
        msg = "%s: %s * %s: %s: %s" % (repo, author, rev, final_path, comment.strip())
    else:
        msg = "[%s] %s: %s * %s: %s: %s" % (date, repo, author, rev, final_path, comment.strip())
    return msg

if __name__ == '__main__': 
    print(__doc__.strip())
