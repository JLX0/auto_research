# Minimal Makefile for Sphinx documentation
#
# This Makefile automates common tasks for Sphinx documentation, such as building
# various output formats, testing documentation examples, and cleaning up artifacts.

# You can set these variables from the command line or override them when calling make.
SPHINXOPTS    = -W --keep-going
# Options passed to sphinx-build (-W treats warnings as errors, --keep-going continues on errors)
SPHINXBUILD   = sphinx-build
# Command to invoke the Sphinx build process
SPHINXPROJ    = package_name
# Name of the Sphinx project
SOURCEDIR     = source
# Directory containing the source documentation files
BUILDDIR      = build
# Directory where the built files will be output

# Default target: "make" without arguments will execute this target.
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
# Displays a list of available Sphinx build commands and options.

.PHONY: help Makefile clean

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
# Catch-all target: Redirects any unknown make targets to Sphinx's "-M" mode.
# The "$@" variable substitutes the name of the invoked target.

doctest:
	sphinx-apidoc -o source/target_code target_code --force --separate --module-first
	sphinx-autogen source/**/*.rst
	@$(SPHINXBUILD) -M doctest "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


clean:
	# Remove build directory
	rm -rf $(BUILDDIR)/*
	
	# Remove auto-generated directories
	rm -rf $(SOURCEDIR)/_examples_gallery
	rm -rf $(SOURCEDIR)/_api_gallery
	rm -rf $(SOURCEDIR)/generated
	rm -rf $(SOURCEDIR)/_autosummary
	
	# Remove Sphinx gallery cache
	rm -rf $(SOURCEDIR)/_examples_python
	rm -rf $(SOURCEDIR)/_examples_jupyter
	
	# Remove execution times and other generated files
	rm -f $(SOURCEDIR)/sg_execution_times.rst
	rm -f $(SOURCEDIR)/_examples_gallery/sg_execution_times.rst
	rm -f $(SOURCEDIR)/_api_gallery/sg_execution_times.rst
	
	# Remove any temporary or cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +