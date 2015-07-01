import weakref
import logging

logger = logging.getLogger(__name__)


class MementoMetaclass(type):
    """
    Classes that use this caching metaclass will have their instances
    automatically cached based on instantiation-time arguments (i.e. to __init__).
    Super-useful for not repetitively creating expensive-to-create objects.

    See http://code.activestate.com/recipes/286132-memento-design-pattern-in-python/
    """
    cache = weakref.WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        key = (self.__name__, ) + args + tuple(sorted(kwargs.items()))
        key = repr(key)
        # logger.debug("Memento: %s args: %s kwargs: %s key: %s",
        #              self.__name__, args, kwargs, key)
        try:
            return self.cache[key]
        except KeyError:
            instance = type.__call__(self, *args, **kwargs)
            self.cache[key] = instance
            return instance
