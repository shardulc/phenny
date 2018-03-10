#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
choose.py - sometimes you just can't decide, a phenny module
"""

import random
import re

def choose(phenny, input):
    """.choose <red> <blue> - for when you just can't decide"""
    origterm = input.groups()[1]
    if not origterm:
        return phenny.say(".choose <red> <blue> - for when you just can't decide")
    c = re.findall(r'([^, ]+)', origterm)
    fate = random.choice(c).strip()
    return phenny.reply("%s" % (fate))
choose.rule = (['choose'], r'(.*)')

if __name__ == '__main__': 
    print(__doc__.strip())
