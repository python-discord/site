from wiki.plugins.macros.mdx import toc

# Remove the toc header prefix. There's no option for this, so we gotta monkey patch it.
toc.HEADER_ID_PREFIX = ''
