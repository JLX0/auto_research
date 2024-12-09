"""
Example Module for Sphinx Gallery
=================================

This script demonstrates a simple example of:
- Computing the square of a number.
- Plotting the function y = x^2 using matplotlib.

Example Usage:
--------------
Run this script to see the output and generated plot:

>>> compute_square(3)
9

>>> compute_square(1.5)
2.25
"""

# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt


def compute_square(number):
    """
    Compute the square of a number.

    Parameters
    ----------
    number : int or float
        The number to be squared.

    Returns
    -------
    int or float
        The square of the input number.

    Examples
    --------
    >>> compute_square(3)
    9

    >>> compute_square(1.5)
    2.25
    """
    return number ** 2


# Example: Generate a range of numbers and compute squares
if __name__ == "__main__":
    # Generate a range of numbers from -10 to 10
    x = np.linspace(-10, 10, 100)

    # Compute the square of each number
    y = compute_square(x)

    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label="y = x^2", color="blue", linestyle="--")
    plt.title("Plot of y = x^2")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color="black", linewidth=0.5, linestyle=":")
    plt.axvline(0, color="black", linewidth=0.5, linestyle=":")
    plt.legend()
    plt.grid(True)

    # Display the plot (managed automatically by Sphinx Gallery)
    plt.show()
