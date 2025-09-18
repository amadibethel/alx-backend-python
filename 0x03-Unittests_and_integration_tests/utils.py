#!/usr/bin/env python3
"""
Utility functions for ALX backend Python projects.
"""

from typing import Any, Dict, Tuple
import requests
from functools import wraps


def access_nested_map(nested_map: Dict, path: Tuple) -> Any:
    """
    Access a nested map using a sequence of keys.

    Args:
        nested_map (dict): The dictionary to traverse.
        path (tuple): A sequence of keys representing the path.

    Returns:
        Any: The value found at the path.

    Raises:
        KeyError: If any key in the path is not found.
    """
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(repr(key))
        current = current[key]
    return current


def get_json(url: str) -> Dict:
    """
    Get the JSON content from a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        dict: The parsed JSON response.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """
    Decorator to cache a method's result in a property.

    Args:
        fn (Callable): Method to memoize.

    Returns:
        property: Cached property.
    """

    @property
    @wraps(fn)
    def wrapper(self):
        attr_name = f"_{fn.__name__}"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return wrapper
