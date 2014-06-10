#!/usr/bin/env python3

import json

class BaltimoreJSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            #print 'MODULE:', module
            class_ = getattr(module, class_name)
            #print 'CLASS:', class_
            args = dict( (key.encode('ascii'), value) for key, value in list(d.items()))
            #print 'INSTANCE ARGS:', args
            inst = class_(**args)
        else:
            inst = d
        return inst
