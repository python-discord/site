from wiki.plugins.macros.mdx import toc

# Remove the toc header prefix. There's no option for this, so we gotta monkey patch it.
toc.HEADER_ID_PREFIX = ''

# Empty list of validators for Allauth to ponder over. This is referred to in settings.py
# by a string because Allauth won't let us just give it a list _there_, we have to point
# at a list _somewhere else_ instead.
VALIDATORS = []
