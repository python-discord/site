from django import template

register = template.Library()


@register.filter
def get_category_icon(name: str) -> str:
    """Get icon of a specific resource category."""
    icons = {
        "Algorithms And Data Structures": "fa-cogs",
        "Data Science": "fa-flask",
        "Databases": "fa-server",
        "Game Development": "fa-joystick",
        "General": "fa-book",
        "Microcontrollers": "fa-microchip",
        "Other": "fa-question-circle",
        "Software Design": "fa-paint-brush",
        "Testing": "fa-vial",
        "Tooling": "fa-toolbox",
        "User Interface": "fa-desktop",
        "Web Development": "fa-wifi",
        "Discord Bots": "fa-robot",
        "Book": "fa-book",
        "Community": "fa-users",
        "Course": "fa-chalkboard-teacher",
        "Interactive": "fa-mouse-pointer",
        "Podcast": "fa-microphone-alt",
        "Tool": "fa-tools",
        "Tutorial": "fa-clipboard-list",
        "Video": "fa-video",
        "Free": "fa-first-aid",
        "Paid": "fa-sack",
        "Subscription": "fa-credit-card",
        "Beginner": "fa-play-circle",
        "Intermediate": "fa-align-center"
    }
    icon_name = icons[name]
    return f'fa {icon_name}'
