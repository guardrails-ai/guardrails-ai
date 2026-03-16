import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "Guardrails AI Types"
copyright = "2024, Guardrails AI"
author = "Guardrails AI"
release = "0.4.0"

extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_markdown_builder",
]

# sphinx-autoapi: scan src/ without needing to import the package
autoapi_type = "python"
autoapi_dirs = ["../src"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_python_class_content = "both"  # include both class and __init__ docstrings
autoapi_member_order = "groupwise"
suppress_warnings = [
    "autoapi.python_import_resolution",
    "ref.python",
    # sphinx-autoapi emits duplicate member descriptions for str(Enum) subclasses;
    # this is a known upstream bug and cannot be suppressed via suppress_warnings.
]

# Napoleon: support Google and NumPy docstring styles
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# intersphinx: link to external docs
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# MyST: allow markdown source files
myst_enable_extensions = ["colon_fence", "deflist"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

html_theme = "furo"
html_static_path = ["_static"]
html_title = "Guardrails AI Types"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
