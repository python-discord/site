from wiki.apps import WikiConfig


class WikiContainerConfig(WikiConfig):
    name = 'wiki_container'
    default_site = 'pydis_site.sites.PyDisWikiSite'
