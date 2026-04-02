import os
import sys

# ---------------------------------------------------------------------------
# Unified source directory for sphinx-autoapi
# ---------------------------------------------------------------------------
# guardrails_ai is a namespace package split across sdk/py/src and types/py/src.
# autoapi doesn't handle multiple roots with the same basename ("src") well —
# it treats "src" itself as a namespace, generating docs under autoapi/src/…
# instead of autoapi/guardrails_ai/…
#
# Fix: build a _packages/guardrails_ai/ directory at conf-load time with
# symlinks into each sub-package so autoapi sees one coherent package tree.
_here = os.path.dirname(os.path.abspath(__file__))
_guardrails_dir = os.path.join(_here, "_packages", "guardrails_ai")

os.makedirs(_guardrails_dir, exist_ok=True)

# Empty __init__.py so autoapi treats guardrails_ai as a regular package.
open(os.path.join(_guardrails_dir, "__init__.py"), "w").close()

for _name, _rel in [
    ("sdk", "../sdk/py/src/guardrails_ai/sdk"),
    ("types", "../types/py/src/guardrails_ai/types"),
]:
    _link = os.path.join(_guardrails_dir, _name)
    _target = os.path.abspath(os.path.join(_here, _rel))
    if os.path.islink(_link):
        os.unlink(_link)
    os.symlink(_target, _link)

sys.path.insert(0, os.path.join(_here, "_packages"))
sys.path.insert(0, os.path.join(_here, "../sdk/py/src"))
sys.path.insert(0, os.path.join(_here, "../types/py/src"))

# ---------------------------------------------------------------------------

project = "Guardrails AI"
copyright = "2024, Guardrails AI"
author = "Guardrails AI"

extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

# sphinx-autoapi: scan the unified _packages/ directory
autoapi_type = "python"
autoapi_dirs = ["_packages"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_follow_symlinks = True
autoapi_python_class_content = "both"
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

source_suffix = {
    ".rst": "restructuredtext",
}

html_theme = "furo"
html_static_path = ["_static"]
html_title = "Guardrails AI"

templates_path = ["_templates"]
exclude_patterns = ["_build", "_packages", "Thumbs.db", ".DS_Store"]
