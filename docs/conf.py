# Sphinx configuration for the ERF-Fire documentation.
#
# The pages are written in Markdown and read by MyST, so the same files render
# on GitHub and on the published site (https://erf-model.github.io/ERF-Fire/).
# Build locally with:
#   python3 -m pip install -r docs/requirements.txt
#   sphinx-build -W --keep-going -b html docs _build/html

project = "ERF-Fire"
author = "The ERF developers"
copyright = "2026, The ERF developers"

extensions = ["myst_parser", "sphinx.ext.intersphinx", "sphinx.ext.mathjax"]

# The FLARE pages in docs/flare/ are reStructuredText copied from erf-model/FLARE
# by tools/sync_flare_docs.py; the hand-written pages are Markdown.
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}

# A :ref: in the FLARE pages to an ERF section (for example sec:FireCoupling)
# resolves against the ERF documentation.
intersphinx_mapping = {"erf": ("https://erf.readthedocs.io/en/latest/", None)}

# Numbered figures and tables, as in the ERF and FLARE documentation.
numfig = True
root_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Anchors for headings down to level 3, so links such as page.md#inputs resolve.
myst_heading_anchors = 3

html_theme = "sphinx_rtd_theme"
html_title = "ERF-Fire"
