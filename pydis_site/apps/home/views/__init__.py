from .account import DeleteView as AccountDeleteView, SettingsView as AccountSettingsView
from .home import HomeView
from .tags import DetailView as TagsDetailView, ListView as TagsListView


__all__ = ["AccountDeleteView", "AccountSettingsView", "HomeView", "TagsDetailView", "TagsListView"]
