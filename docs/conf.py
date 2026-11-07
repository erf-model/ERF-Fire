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

extensions = ["myst_parser"]

source_suffix = {".md": "markdown"}
root_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Anchors for headings down to level 3, so links such as page.md#inputs resolve.
myst_heading_anchors = 3

html_theme = "sphinx_rtd_theme"
html_title = "ERF-Fire"
