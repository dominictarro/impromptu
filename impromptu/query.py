"""
A class for constructing Query hierarchies with inheritance, deconstructing hierarchies into Python
dictionaries, and searching hierarchies for labeled Queries.
"""
from __future__ import annotations
from typing import Any, Dict, List, OrderedDict
from collections import OrderedDict as odict
from mongoquery import Query as mQuery
from .base import TreeBase

MISSING = type('MISSING', (), {})
ASSIGN = '$assign'

class Query(TreeBase):
    """A node in the tree of Query objects.
    """

    __slots__ = ['_raw_definition', '_definition', '_label', '_parent', '_children', '_mongoquery']

    def __init__(
        self, definition: Dict[Any, Any],
        label: str = '#root',
        parent: Query = None,
        children: OrderedDict[str, Query] = None
        ):
        self._raw_definition: Dict[Any, Any] = definition.copy()
        self._definition: Dict[Any, Any] = definition.copy()
        self._label: str = label
        self._parent: Query = parent
        self._children: OrderedDict[str, Query] = odict()
        if children is not None:
            self._children.update(children)
        self._inherit()
        self._init_children()
        self._mongoquery: mQuery = mQuery(self._definition)
        super().__init__()

    def __repr__(self) -> str:
        return f"<Query {'.'.join(q.label for q in self.inheritance)}>"

    def __getitem__(self, label: str) -> Query:
        return self._children.get(label)

    @property
    def children(self) -> OrderedDict[str, Query]:
        """A copy of the Query's children.
        """
        return self._children.copy()

    @property
    def definition(self) -> Dict[Any, Any]:
        """A copy of the Query's definition.
        """
        return self._definition.copy()

    @property
    def inheritance(self) -> List[Query]:
        """Creates a list of the Query(s) that the Query inherits from, down to itself.
        """
        return (self.parent.inheritance if isinstance(self.parent, Query) else []) + [self]

    @property
    def label(self) -> List[Query]:
        """The Query's text label.
        """
        return self._label

    @property
    def parent(self) -> Query:
        """The Query's parent Query.
        """
        return self._parent

    def _inherit(self):
        """Inherits the parent's definition, overriding conflicts with the Query's own definition.
        """
        inheritance = {
            k: v
            for k, v in self._parent.definition.items()
            if (
                not isinstance(v, dict) # is not a dictionary value
                or v.get(ASSIGN, None) is None # is not a dict with the assignment operator
                )
            } if isinstance(self._parent, Query) else {}
        self._definition = dict(inheritance, **self._definition)

    def _init_children(self):
        """Initializes all children Queries found within the definition. Overrides any existing.
        """
        for key, _def in self._raw_definition.items():
            if isinstance(_def, dict) and ASSIGN in _def:
                # remove the assignment declaration from the parent's query definition
                _scoped = self._definition.pop(key).get(ASSIGN)
                self._children[key] = Query(
                                        _scoped,
                                        label=key,
                                        parent=self
                                    )

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
        if label in ('', self._label):
            return self
        if '.' in label:
            # use period delimiter to denote a parent-child relationship
            _labels = label.split('.')
            node: Query = self
            for _label in _labels:
                # this will raise an error if the child does not exist for one of the nodes
                node = node.get(_label)
            return node
        return self._children.get(label)

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
            begin (str, optional):      Begin searching at this Query's child node specified in the
                                        string. Children of children should be delimited with a
                                        period, e.g. childA.childAA.childAAA... Do not include this
                                        Query's node.

        Raises:
            ValueError: An invalid tree searching method was provided.

        Returns:
            Query:  A Query that matches the given label, or the default value if no matching
                    Query is found.
        """
        # NOTE, all algorithms will return the FIRST matching query. Reused labels will be lost,
        # unless a starting node is selected where the desired Query's label is first (of the
        # redundant uses).
        # Example
        # root  - aQuery (1)
        #           - aQuery (1.a)
        #           - bQuery (1.b)
        #       - bQuery (2)
        # Using depth first from root, searching aQuery will yield the node marked 1 and searching
        # bQuery will yield the node marked 1.b
        #
        # Using breadth first from root, aQuery will yield node 1 and bQuery will yield node 2
        if begin is not None:
            node = self.get(begin)
            return node.search(label=label, default=default, method=method)
        if label in ('', self._label):
            return self
        if method == 'depth':
            return self._search_depth(label=label, default=default)
        if method == 'breadth':
            return self._search_breadth(label=label, default=default)
        raise ValueError(f"method '{method}' is not supported. Try 'depth' or 'breadth'")

    def _search_breadth(self, label: str, default = None) -> Query:
        """Breadth-first algorithm for finding the first query to match a label.

        Args:
            label (str): Label of the Query to return.
            default ([type], optional): Value to return if no match is found for the label.
                                        Defaults to None.

        Returns:
            Query:  A Query that matches the given label, or the default value if no matching Query
                    is found.
        """
        children: List[OrderedDict[str, Query]] = [self._children]
        try:
            while True:
                child = children.pop(0)
                candidate = child.get(label, None) # dict method, not Query method
                if candidate is not None:
                    return candidate
                for child in child.values():
                    children.append(child.children)
        except IndexError:
            return default

    def _search_depth(self, label: str, default = None) -> Query:
        """Depth-first algorithm for finding the first query to match a label.

        Args:
            label (str): Label of the Query to return.
            default ([type], optional): Value to return if no match is found for the label.
                                        Defaults to None.

        Returns:
            Query:  A Query that matches the given label, or the default value if no matching Query
                    is found.
        """
        for child in self._children.values():
            candidate = child.search(label, method='depth')
            if candidate is not None:
                return candidate
        return default

    def jsonify(self, deduplicate: bool = True) -> Dict[Any, Any]:
        """Returns the Query to a JSON document, including the JSON form of all children. The JSON
        document can be reused for reconstructing the Query tree.

        Args:
            deduplicate (bool, optional):   Removes inherited expressions in all children. Defaults
                                            to True.

        Returns:
            Dict[Any, Any]: The definition in JSON format
        """
        _def = self.definition
        if deduplicate:
            for child in self._children.values():
                _def[child.label] = {ASSIGN: {}}
                for key, value in child.jsonify(deduplicate=True).items():
                    # the expression variable originates from the user's passed definition and
                    # should always be a JSON supported type (not the Missing type)
                    _def_value = _def.get(key, MISSING)
                    if _def_value == MISSING or _def_value != value:
                        # if the child modified the expression or the expression is missing from
                        # the parent, it is unique to the child
                        _def[child.label][ASSIGN][key] = value
        else:
            for child in self._children.values():
                _def[child.label] = {ASSIGN: child.jsonify(deduplicate=False)}
        return _def

    def match(self, entry: Dict[Any, Any]) -> bool:
        """Matches an entry document against the Query definition.

        Args:
            entry (Dict[Any, Any]): A document representing the keys and arguments that will be
                                    matched against the definition's conditions.

        Returns:
            bool: The entry meets the definition's conditions
        """
        return self._mongoquery.match(entry=entry)
