"""Impromptu class for creating and using Query filters.

Check https://github.com/kapouille/mongoquery for supported MongoDB query syntax.
"""
from __future__ import annotations
import functools
import json
from typing import Any, Callable, Dict, Mapping, Union
from .argdefiner import ArgDefiner
from .base import TreeBase
from .query import Query
from .utils import Singleton


class Impromptu(Singleton, TreeBase):
    """Uses MongoDB-style queries to approve or disapprove of passed arguments.

    See https://github.com/kapouille/mongoquery for the supported mongoquery syntax.

    Labeled queries inherit all parent parameters unless overriden. For example
    {
        'a': 0,
        'b': 1,
        'andC': {
            '$assign': {
                'c': 0
            }
        },
        'aNot0': {
            '$assign': {
                'a': {
                    '$not': 0
                }
            }
        }
    }
    has three Query objects. The first is the root query, which can be accessed with the label ''
    or '#root'. The next are the child Queries, 'andC' and 'aNot0'. andC's verbose definition is
    {'a': 0, 'b': 1, 'c': 0}, however with the impromptu syntax it can simply inherit the
    expression {'a': 0, 'b': 1}.

    aNot0 overrides the expression {'a': 0} while still inheriting the expression {'b': 1}. Its
    verbose definition is {'a': {'$not': 0}, 'b': 1}.
    """
    _root: Query

    @property
    def root(self) -> Query:
        """The root Query within the Query tree

        Returns:
            Query: Root Query
        """
        return self._root

    def __repr__(self) -> str:
        return self._root.__repr__()

    def set_root(self, query: Query):
        """Sets the root attribute with a new query.

        Args:
            query (Query): Query to set as root
        """
        self._root = query

    ##########
    # abstract
    ##########

    def get(self, label: str) -> Query:
        """Retrieves the Query matching this label or inheritance sequence of labels.

        Args:
            label (str):    Get the child node specified in the spring. Children of children should
                            be delimited with a period, e.g. childA.childAA.childAAA... Do not
                            include this Query's node.

        Raises:
            KeyError: Child Query does not exist

        Returns:
            Query: Child Query whose label matches the given
        """
        return self._root.get(label)

    def search(
        self,
        label: str,
        default: Any = None,
        method: str = 'depth',
        begin: str = None
        ) -> Query:
        """Finds the first Query object whose label matches the given. If none are found, a default
        value is returned. Can search via a depth-first or breadth-first algorithm.

        Args:
            label (str): Label of the Query to return.
            default (Any, optional):    Value to return if no match is found for the label.
                                        Defaults to None.
            method (str, optional):     Tree-searching method to use ('depth' or 'breadth').
                                        Defaults to 'depth'.
            begin (str, optional):      Begin searching at this Query's child node specified in
                                        the string. Children of children should be delimited with
                                        a period, e.g. childA.childAA.childAAA... Do not include
                                        this Query's node.

        Raises:
            ValueError: An invalid tree searching method was provided.

        Returns:
            Query:  A Query that matches the given label, or the default value if no matching Query
                    is found.
        """
        return self._root.search(label, default=default, method=method, begin=begin)

    def jsonify(self, deduplicate: bool = True) -> Dict[Any, Any]:
        """Returns the Query tree to a JSON document, including the JSON form of all children. The
        JSON document can be reused for reconstructing the Query tree.

        Args:
            deduplicate (bool, optional):   Removes inherited expressions in all children. Defaults
                                            to True.

        Returns:
            Dict[Any, Any]: The definition in JSON format
        """
        return self._root.jsonify(deduplicate=deduplicate)

    ################
    # initialization
    ################

    @classmethod
    def from_string(cls, definition: Union[str, bytes], **kwargs) -> Impromptu:
        """Constructs and returns an Impromptu from a string representation of MongoDB query syntax.
        Additional keyword arguments are passed to the JSON loader.

        Args:
            definition (Union[str, bytes]): Query string

        Returns:
            Impromptu: ...
        """
        return cls.from_dict(json.loads(s=definition, **kwargs))

    @classmethod
    def from_dict(cls, definition: Mapping[str, Any]) -> Impromptu:
        """Constructs and returns an Impromptu from a map representation of MongoDB query syntax.

        Args:
            definition (Dict[str, Any]): Query mapping

        Returns:
            Impromptu: ...
        """
        obj = cls()
        obj.set_root(query=Query(definition=definition))
        return obj

    @classmethod
    def from_file(cls, *args, **kwargs) -> Impromptu:
        """Constructs and returns an Impromptu from a JSON-formatted file using MongoDB query
        syntax.

        Positional and keyword arguments are passed to the json.load method.
        https://docs.python.org/3/library/json.html#json.load

        Returns:
            Impromptu: ...
        """
        return cls.from_dict(json.load(*args, **kwargs))

    ################
    # implementation
    ################

    def __call__(self, entry: Dict[Any, Any], label: str = '') -> bool:
        """Uses the Query associated with label to determine if the entry meets the query
        definition.

        Args:
            entry (Dict[Any, Any]): Arguments to check
            label (str, optional): Query to use. Defaults to #root.

        Returns:
            bool: Entry meets definition
        """
        return self.get(label=label).match(entry=entry)

    def match(self, label: str = '', **kwds) -> bool:
        """Match a mapping of keyword arguments against the query definition for the given filter.

        Args:
            label (str, optional): Query to use. Defaults to #root.

        Returns:
            bool: Keywords match filter definition.
        """
        return self.__call__(entry=kwds, label=label)

    def on_match(
        self,
        label: str = '',
        false_return_value: Any = None,
        true_if_missing: bool = False,
        discovery_method: str = 'get',
        inverse: bool = False,
        **kwds
        ) -> Callable:
        """Wrapper that matches arguments against a query to determine whether the function should
        be executed.

        Args:
            label (str, optional): Query to use. Defaults to ''.
            false_return_value (Any, optional): Value to return if the arguments do not match the
                                                definition. Defaults to None.
            inverse (bool, optional):           If the match fails, execute the function. If it
                                                succeeds, return false_return_value. Defaults to
                                                False.
            true_if_missing (bool, optional):   If the label cannot be found, execute the function.
                                                Defaults to False.
            discovery_method (str, optional):   Method to use for acquiring the Query node to be
                                                used. Defaults to 'get'.
            **kwds: Keyword arguments to pass to the search method.

        Returns:
            Callable: Function that is only called when parameters meet Query definition.
        """
        def decorator(func: Callable) -> Callable:

            arg_definer = ArgDefiner(func)
            node: Query = self._root

            if discovery_method == 'get':
                try:
                    node = self.get(label=label)
                except KeyError:
                    node = None
            elif discovery_method == 'search':
                node = self.search(label=label, **kwds)
            else:
                msg=f"discovery method '{discovery_method}' is not supported. \
                    Try 'get' or 'search'"
                raise ValueError(msg)

            logical: Callable = lambda entry: node.match(entry=entry)
            if inverse:
                logical = lambda entry: node.match(entry=entry) is False

            if node is None:
                logical = lambda entry: true_if_missing

            @functools.wraps(func)
            def wrapper(*args, **kwds) -> Any:
                defined = arg_definer.define(args, kwds, restriced=False)
                if logical(entry=defined):
                    args, kwds = arg_definer.package(args, kwds)
                    return func(*args, **kwds)
                return false_return_value

            return wrapper
        return decorator
