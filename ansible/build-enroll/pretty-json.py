#!/usr/bin/env python

import os
import sys
import json

file = sys.argv[1]

with open(file) as f:
    data = json.load(f)

print json.dumps(data, indent=4, sort_keys=True)
