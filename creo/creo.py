#!/usr/bin/env python
"""
Module pmcx

:Company: SwissTech Consulting
:Author: Patrick Glass <patrickglass@swisstech.ca>
:Copyright: Copyright 2014 SwissTech Consulting

This software is used for flow development and execution for the
IC Physical Design group.
"""
from functools import wraps

def authenticate(func):
    """
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def follows(func_name):
    """
    """
    def wrapper(func):
        def authorize_and_call(*args, **kwargs):
            if not current_user.has(role): 
                raise Exception('Unauthorized Access!')
            return func(*args, **kwargs)
        return authorize_and_call
    return wrapper



class NullDecl(object):
   def __init__ (self, func):
      self.func = func
      for name in set(dir(func)) - set(dir(self)):
        setattr(self, name, getattr(func, name))

   def __call__ (self, *args):
      return self.func (*args)
