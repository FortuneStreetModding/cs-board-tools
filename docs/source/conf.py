# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cs-board-tools'
copyright = '2023-2024, Custom Street'
author = 'Custom Street'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_copybutton',
    'sphinx-prompt',
    'sphinxemoji.sphinxemoji',
    'myst_parser',
    "sphinx_design",
    'autodocsumm',
    "sphinx.ext.autosectionlabel",
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "both"   # Add __init__ doc (ie. params) to class summaries
add_module_names = False     # Remove namespaces from class/method signatures
autodoc_default_options = {
    'autosummary': True,
}
templates_path = ['_templates']
exclude_patterns = []
myst_enable_extensions = ["colon_fence"]
# Make sure the target is unique
autosectionlabel_prefix_document = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_nefertiti'
html_static_path = ['_static']

html_theme_options = {
    # ... other options ...
    "footer_links": ",".join([
        "Documentation|https://fortunestreetmodding.github.io",
        "Package|https://pypi.com/cs-board-tools",
        "Discord|https://discord.gg/DE9Hn7T",
        "Repository|https://github.com/fortunestreetmodding/cs-board-tools",
        "Issues|https://github.com/fortunestreetmodding/cs-board-tools/issues",
    ]),
    "style": "purple",
    "repository_name": "fortunestreetmodding/cs-board-tools",
    "repository_url": "https://github.com/fortunestreetmodding/cs-board-tools",
    "monospace_font": "luminari",
}
