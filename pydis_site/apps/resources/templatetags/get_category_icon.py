from django import template

register = template.Library()

_ICONS = {
    "Algorithms And Data Structures": "fa-cogs",
    "Beginner": "fa-play-circle",
    "Book": "fa-book",
    "Community": "fa-users",
    "Course": "fa-chalkboard-teacher",
    "Data Science": "fa-flask",
    "Databases": "fa-server",
    "Discord Bots": "fa-robot",
    "Free": "fa-first-aid",
    "Game Development": "fa-joystick",
    "General": "fa-book",
    "Interactive": "fa-mouse-pointer",
    "Intermediate": "fa-align-center",
    "Microcontrollers": "fa-microchip",
    "Other": "fa-question-circle",
    "Paid": "fa-dollar-sign",
    "Podcast": "fa-microphone-alt",
    "Project Ideas": "fa-lightbulb-o",
    "Software Design": "fa-paint-brush",
    "Subscription": "fa-credit-card",
    "Testing": "fa-vial",
    "Tool": "fa-tools",
    "Tooling": "fa-toolbox",
    "Tutorial": "fa-clipboard-list",
    "User Interface": "fa-desktop",
    "Video": "fa-video",
    "Web Development": "fa-wifi",
}


@register.filter
def get_category_icon(name: str) -> str:
    """Get icon of a specific resource category."""
    return f'fa {_ICONS[name]}'
