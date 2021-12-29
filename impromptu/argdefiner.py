"""
Inspects a function's argument structure and matches the passed arguments with their respective
definitions.
"""
from __future__ import annotations
import inspect
from typing import Any, Callable, Dict, Tuple


class ArgDefiner:
    """Inspects a function's signature to infer information about ambigously passed arguments
    such as those in variable arguments and keyword arguments.
    """

    def __init__(self, func: Callable) -> None:
        """Matches the passed positional, keyword and variable positional and keyword arguments to
        the function's names.

        Args:
            func (Callable): function whose argument definitions should be used for association
        """
        self.func: Callable = func
        self.signature: inspect.Signature = inspect.signature(func, follow_wrapped=True)
        self.argspec: inspect.FullArgSpec = inspect.getfullargspec(func)

    def define(
        self,
        args: Tuple[Any],
        kwds: Dict[Any, Any],
        restriced: bool = True
        ) -> Dict[Any, Any]:
        """Associates the given arguments (positional and keywords) to the function's definition.

        Args:
            args (Tuple[Any]):              positional arguments
            kwds (Dict[Any, Any]):          keyword arguments
            restricted (bool, optional):    only include arguments supported by the function
                                            (exclude excess)

        Returns:
            Dict[Any, Any]: function defined arguments associated with passed arguments + excess
        """
        if restriced:
            return self.restrict(args, kwds)
        return self._define(args, kwds)

    def _define(self, args: Tuple[Any], kwds: Dict[Any, Any]) -> Dict[str, Any]:
        """Associates the given arguments (positional and keywords) to the function's definition.
        Will include any variable positional or keyword arguments not found in the function's
        definition. Variable keywords will be indistinguishable from defined keywords, however
        variable positionals will use the varargs name or None if the varargs name is not defined
        in the function.

        Args:
            args (Tuple[Any]): positional arguments
            kwds (Dict[Any, Any]): keyword arguments
            restricted (bool, optional): exclude excess arguments not supported by the function

        Returns:
            Dict[Any, Any]: function defined arguments associated with passed arguments + excess
        """
        # positional
        argmap = dict(zip(self.argspec.args, args))

        # positional or keyword default
        # start at the end of non-default positional arguments
        for k in self.argspec.args[len(argmap):]:
            argmap[k] = kwds.get(k, self.signature.parameters.get(k).default)

        # varargs
        # start at the end of positional arguments
        argmap[self.argspec.varargs] = tuple(v for v in args[len(argmap):])

        # keyword defaults
        for k in self.argspec.kwonlyargs:
            argmap[k] = self.signature.parameters.get(k).default

        # passed keywords (defined and variable)
        argmap.update(kwds)

        return argmap

    def restrict(self, args: Tuple[Any], kwds: Dict[Any, Any]) -> Dict[str, Any]:
        """Performs a define, but only using the positional and keyword arguments defined in the
        function. Variable arguments are not included unless included within the function.

        Args:
            args (Tuple[Any]): positional arguments
            kwds (Dict[Any, Any]): keyword arguments

        Returns:
            Dict[str, Any]: function defined arguments associated with passed arguments
        """
        # positional
        argmap = dict(zip(self.argspec.args, args))

        # positional or keyword default
        # start at the end of non-default positional arguments
        for k in self.argspec.args[len(argmap):]:
            argmap[k] = kwds.pop(k, self.signature.parameters.get(k).default)

        # keyword defaults
        for k in self.argspec.kwonlyargs:
            argmap[k] = kwds.pop(k, self.signature.parameters.get(k).default)

        # variable args
        if self.argspec.varargs is not None:
            argmap[self.argspec.varargs] = tuple(v for v in args[len(argmap):])

        # variable keywords
        if self.argspec.varkw is not None:
            # should be the remaining keywords
            argmap[self.argspec.varkw] = kwds
        return argmap

    def package(self, args: Tuple[Any], kwds: Dict[Any, Any]) -> Tuple[Tuple[Any], Dict[Any, Any]]:
        """Packages the function's defined positional and keyword arguments into a tuple and
        dictionary that can be unpacked for the method. Prevents excess arguments from being
        passed to the function.

        Args:
            args (Tuple[Any]):      positional arguments to consider
            kwds (Dict[Any, Any]):  keyword arguments to consider

        Returns:
            Tuple[Tuple[Any], Dict[Any, Any]]: the arguments
        """
        _args = args[:len(self.argspec.args)]
        _arglen = len(_args)

        if self.argspec.varargs is not None and _arglen < len(args):
            _args = args
            _arglen = len(args)

        _kwds = {
            k: kwds.pop(k, self.signature.parameters.get(k).default)
            for k in self.argspec.args[_arglen:]
        }

        # keyword passed or default
        for k in self.argspec.kwonlyargs:
            _kwds[k] = kwds.pop(k, self.signature.parameters.get(k).default)

        # variable keywords
        if self.argspec.varkw is not None:
            # should be the remaining keywords
            _kwds.update(kwds)

        return _args, _kwds

    def call(self, *args, **kwds) -> Any:
        """Derives arguments to pass to the function given its definition.

        Returns:
            Any: The value returned from the function given the arguments.
        """
        pck = self.package(args, kwds)
        return self.func(*pck[0], **pck[1])
