# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
#import os
#import sys
#sys.path.insert(0, os.path.abspath('../..'))

import geowombat as gw


# -- Project information -----------------------------------------------------

project = 'GeoWombat'
copyright = '2019, GeoWombat'
author = ''

# The full version, including alpha/beta/rc tags
release = gw.__version__


# -- General configuration ---------------------------------------------------

# Should special members (like __membername__) and private members
# (like _membername) members be included in the documentation if they
# have docstrings.
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['IPython.sphinxext.ipython_directive',
              'IPython.sphinxext.ipython_console_highlighting',
              'sphinx.ext.mathjax',
              'sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.inheritance_diagram',
              'sphinx_automodapi.automodapi',
              'sphinx.ext.napoleon',
              'sphinxcontrib.bibtex',
              'numpydoc']

# mathjax_path = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {'page_width': '80%',
                      'fixed_sidebar': True,
                      'logo': 'logo.png',
                      'logo_name': False,
                      'github_banner': True,
                      'github_button': True,
                      'github_user': 'jgrss',
                      'github_repo': 'geowombat',
                      'anchor': '#d37a7a',
                      'anchor_hover_bg': '#d37a7a',
                      'anchor_hover_fg': '#d37a7a'}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

