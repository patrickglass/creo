import logging


logger = logging.getLogger(__name__)


class TaskRegisterMemento(type):
    """
    This class implements two separate features. It will ensure that all
    class instances of the same name and arguments return the same cached
    object. Second it will register each defined class and use this information
    to build the list of defined tasks which can be run by name.
    """

    def __init__(self, name, bases, attrs):
        """
        When a new class is created we want to store a reference by name
        so that we can have a procedure to list all created Tasks. This also`
        allows referencing classes by name and able to retrieve an instance of
        it. We want register to be separate for each new metaclass usage so
        we must store the references in the base instance.

        :param name: name of the class
        :param bases: tuple of all base classes
        :param attrs: dictionary of attributes for the new class
        """
        if not hasattr(self, 'class_register'):
            self.class_register = {}

        # Create the class dictionary for storing instances
        if not hasattr(self, 'instance_cache'):
            self.instance_cache = {}

        self.class_register[name] = self

        super(TaskRegisterMemento, self).__init__(name, bases, attrs)

    def __call__(self, *args, **kwargs):
        """
        Call is used when a new class is instantiated. We want to have new
        instances which have the same arguments to be the same object as their
        predecessor. This is done with a instance cache which is keyed on the
        class name and arguments. This ensure that expensive run operations,
        only need to be done for once instances and all following tasks just
        reference this same object.

        See http://code.activestate.com/recipes/286132-memento-design-pattern-in-python/

        :param name: name of the class
        :param bases: tuple of all base classes
        :param attrs: dictionary of attributes for the new class
        "
        """
        key = (self.__name__, ) + args + tuple(sorted(kwargs.items()))
        key = repr(key)
        try:
            return self.instance_cache[key]
        except KeyError:
            instance = super(TaskRegisterMemento, self).__call__(*args, **kwargs)
            self.instance_cache[key] = instance
            return instance

    @property
    def classes(self):
        return self.class_register

    @property
    def instances(self):
        return self.instance_cache

    def class_by_name(self, task_class_name):
        return self.class_register[task_class_name]
