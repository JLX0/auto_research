"""Example Module for Documentation
=================================

This module demonstrates proper documentation formatting for Sphinx.
It includes example classes and functions with proper docstrings.
"""

class ExampleClass:
    """A demonstration class for documentation purposes.
    
    This class shows how to properly document a Python class using
    Google-style docstrings that Sphinx can parse.

    Attributes:
        name (str): The name of the instance
        value (int): A numeric value associated with the instance
    """

    def __init__(self, name: str, value: int = 0):
        """Initialize the ExampleClass.

        Args:
            name (str): The name to assign to the instance
            value (int, optional): Initial value. Defaults to 0.
        """
        self.name = name
        self.value = value

    def increment_value(self, amount: int = 1) -> int:
        """Increment the instance's value.

        Args:
            amount (int, optional): Amount to increment by. Defaults to 1.

        Returns:
            int: The new value after incrementing
        """
        self.value += amount
        return self.value


def example_function(param1: str, param2: int = 42) -> dict:
    """An example function with proper documentation.

    This function demonstrates how to document parameters,
    return values, and include examples in the docstring.

    Args:
        param1 (str): First parameter description
        param2 (int, optional): Second parameter description. Defaults to 42.

    Returns:
        dict: A dictionary containing the processed parameters

    Examples:
        >>> result = example_function("test", 123)
        >>> print(result)
        {'param1': 'test', 'param2': 123}
    """
    return {
        "param1": param1,
        "param2": param2
    }