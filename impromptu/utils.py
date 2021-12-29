"""
Utility classes and functions.

"""
from typing import Dict

class Singleton:
    """A class where only one instance can exist.
    """

    _instances: Dict[str, object] = {}

    def __new__(cls, *args, **kwds) -> object:
        """Returns an existing instance or creates a new instance of the class.
        Returns:
            object: An instance of the class
        """
        instance = Singleton._instances.get(cls, None)
        if instance is None:
            Singleton._instances[cls] = super().__new__(cls)
            Singleton._instances[cls].__init__(*args, **kwds)
            instance = Singleton._instances[cls]
        return instance

    def abandon(self):
        """Abandons the existing instance, allowing for a new instance of the class.
        """
        Singleton._instances.pop(type(self))
