from __future__ import annotations

import warnings

import fitz


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename by removing illegal characters that are not allowed in Windows filenames.

    Args:
        filename (str): The original filename to be sanitized.

    Returns:
        str: The sanitized filename with illegal characters removed and leading/trailing spaces
        stripped.

    Example:
        >>> sanitize_filename("my/file:name?.txt")
        'myfilename.txt'
    """
    illegal_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
    for char in illegal_chars:
        filename = filename.replace(char, "")
    return filename.strip()


def is_pdf_uncorrupted(file_path: str) -> bool:
    """
    Checks if a PDF file is uncorrupted by attempting to open it using the `fitz` library.

    Args:
        file_path (str): The path to the PDF file to be checked.

    Returns:
        bool: True if the PDF is not corrupted and can be opened successfully, False otherwise.

    Example:
        >>> is_pdf_uncorrupted("example.pdf")
        True
        >>> is_pdf_uncorrupted("corrupted.pdf")
        Error opening PDF: <error message>
        False

    Notes:
        This function uses the `fitz` library (PyMuPDF) to open the PDF file. If the file cannot be
        opened, it is assumed to be corrupted, and the function returns False.
    """
    try:
        doc = fitz.open(file_path)
        doc.close()
        return True
    except Exception as e:
        warnings.warn(f"Error opening PDF: {e}", UserWarning)
        return False
