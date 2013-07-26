#!/usr/bin/env python2.7

import json

class BaltimoreJSONEncoder(json.JSONEncoder):
    def default(self, obj):
#        print 'default(', repr(obj), ')'
        d = { '__class__':obj.__class__.__name__,
                '__module__':obj.__module__, }
        d.update(obj.__dict__)
        return d
