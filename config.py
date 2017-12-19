#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import types


class Config:
    
    def from_pyfile(self, filename, silent=False):
        #filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True
    
    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                #self[key] = getattr(obj, key)
                setattr(self, key, getattr(obj, key))
                
    def __str__(self):
        result = []
        for key in dir(self):
            if key.isupper():
                result.append((key, getattr(self,key)))
        return str(result)


def load_config(config_path=None):
    
    if config_path is None:
        import __main__ as main
        main_path = os.path.dirname(os.path.realpath(main.__file__))
        config_path = os.path.join(main_path, 'my_config.py')
    
    print('loading config file: {}'.format(config_path))
    cfg = Config()
    cfg.from_pyfile(config_path)
    print('config loaded')
    return cfg