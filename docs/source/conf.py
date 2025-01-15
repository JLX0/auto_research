# flake8: noqa
# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# For a complete list of options, see:
# http://www.sphinx-doc.org/en/master/config

# -- Settings -------------------------------------------------

package_name = "auto_research"
author = "Jinglue XU"

github_username = "JXL0"

version = "0.1.0"
release = "0.1.0"

# -- Path setup --------------------------------------------------------------

import os
import sys


# Add the path to your package's source code
def add_target_code_paths(target_dir):
    for root, dirs, files in os.walk(target_dir):
        sys.path.insert(0, os.path.abspath(root))


# Include paths for the package dynamically
add_target_code_paths(f"./target_code/{package_name}")

import warnings

from sklearn.exceptions import ConvergenceWarning


# -- General configuration ---------------------------------------------------

project = package_name

# Define the root document
root_doc = "index"

# Add any Sphinx extension module names here
extensions = [
    "sphinx.ext.autodoc",  # Generate API documentation from docstrings
    "sphinx.ext.autosummary",  # Generate summary tables for API docs
    "sphinx.ext.doctest",  # Test code snippets in documentation
    "sphinx.ext.imgconverter",  # Convert images to appropriate formats
    "sphinx.ext.intersphinx",  # Link to other projects' documentation
    "sphinx.ext.mathjax",  # Render math via MathJax
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx.ext.githubpages",  # Create .nojekyll file for GitHub Pages
    "sphinx_copybutton",  # Add copy buttons to code blocks
    "sphinx_gallery.gen_gallery",  # Generate gallery from Python scripts
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
templates_path = ["_templates"]
source_suffix = ".rst"  # The suffix of source files

# Files to ignore when building documentation
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "examples/GALLERY_HEADER.rst",
    f"target_code/{package_name}/GALLERY_HEADER.rst",
]

# Syntax highlighting style
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages
html_theme = "sphinx_rtd_theme"

# Theme options
html_theme_options = {
    "logo_only": True,
    "navigation_with_keys": True,
    "style_nav_header_background": "#2980B9",
    "style_external_links": True,
}

# The paths that contain custom static files
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

# These paths are either relative to html_static_path or fully qualified paths
html_favicon = None
html_logo = None

# -- Options for LaTeX output ------------------------------------------------

latex_documents = [
    (
        root_doc,
        f"{package_name}.tex",
        f"{package_name} Documentation",
        "Your Name or Organization",
        "manual",
    ),
]

# -- Options for manual page output ------------------------------------------

man_pages = [(root_doc, package_name, f"{package_name} Documentation", [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (
        root_doc,
        package_name,
        f"{package_name} Documentation",
        author,
        package_name,
        "A tool for automated research workflows.",
        "Miscellaneous",
    ),
]

# -- Extension configuration -------------------------------------------------

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "sklearn": ("https://scikit-learn.org/stable", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# Autodoc configuration
autosummary_generate = True
autodoc_typehints = "description"
autodoc_member_order = "bysource"
add_module_names = False
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "undoc-members": True,
}

# Napoleon settings for docstring parsing
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Copy button configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Sphinx Gallery configuration
sphinx_gallery_conf = {
    "doc_module": package_name,
    "examples_dirs": ["examples"],  # Example scripts directory
    "gallery_dirs": ["_examples_gallery"],  # Output directory
    "filename_pattern": r".*\.py",
    "ignore_pattern": r"(^__|GALLERY_HEADER)",
    "compress_images": ("images", "thumbnails"),
    "thumbnail_size": (400, 280),
    "within_subsection_order": "FileNameSortKey",
    "show_memory": True,
    "capture_repr": ("_repr_html_", "__repr__"),
    "backreferences_dir": None,
    "download_all_examples": True,
    "remove_config_comments": True,
    "show_signature": True,
}

# -- Additional settings -----------------------------------------------------

# Default role for text marked up with single backticks
default_role = "any"

# Warnings to ignore
warnings.filterwarnings("ignore", category=ConvergenceWarning, module="sklearn")

# Number figures, tables and code-blocks
numfig = True
numfig_format = {
    "figure": "Figure %s",
    "table": "Table %s",
    "code-block": "Listing %s",
    "section": "Section %s",
}

# If true, show URL addresses after external links
latex_show_urls = "footnote"

# Don't show type hints in signature (they're in the description)
autodoc_typehints_format = "fully-qualified"

# Create a list of external links that can be used throughout the documentation
extlinks = {
    "issue": (f"https://github.com/{github_username}/{package_name}/issues/%s", "#%s"),
    "pull": (f"https://github.com/{github_username}/{package_name}/pull/%s", "PR #%s"),
}
