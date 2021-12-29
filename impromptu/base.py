"""Base classes for package objects.
"""
import abc
from typing import Any


class TreeBase(abc.ABC):
    """Base class for implementing tree-like classes.
    """

    @abc.abstractmethod
    def get(self, label: str):
        """Get the node with a given label."""

    @abc.abstractmethod
    def search(
        self,
        label: str,
        default: Any = None,
        method: str = 'depth',
        begin: str = None
        ):
        """Search for the node with the given label, using the given methods."""

    @abc.abstractmethod
    def jsonify(self, deduplicate: bool = True):
        """Convert the tree into a dictionary meeting JSON format.
        """
