from django.db import migrations

guild_invite_whitelist = [
    ("discord.gg/python", "Python Discord", True),
    ("discord.gg/4JJdJKb", "RLBot", True),
    ("discord.gg/djPtTRJ", "Kivy", True),
    ("discord.gg/QXyegWe", "Pyglet", True),
    ("discord.gg/9XsucTT", "Panda3D", True),
    ("discord.gg/AP3rq2k", "PyWeek", True),
    ("discord.gg/vSPsP9t", "Microsoft Python", True),
    ("discord.gg/bRCvFy9", "Discord.js Official", True),
    ("discord.gg/9zT7NHP", "Programming Discussions", True),
    ("discord.gg/ysd6M4r", "JetBrains Community", True),
    ("discord.gg/4xJeCgy", "Raspberry Pie", True),
    ("discord.gg/AStb3kZ", "Ren'Py", True),
    ("discord.gg/t655QNV", "Python Discord: Emojis 1", True),
    ("discord.gg/vRZPkqC", "Python Discord: Emojis 2", True),
    ("discord.gg/jTtgWuy", "Django", True),
    ("discord.gg/W9BypZF", "STEM", True),
    ("discord.gg/dpy", "discord.py", True),
    ("discord.gg/programming", "Programmers Hangout", True),
    ("discord.gg/qhGUjGD", "SpeakJS", True),
    ("discord.gg/eTbWSZj", "Functional Programming", True),
    ("discord.gg/r8yreB6", "PyGame", True),
    ("discord.gg/5UBnR3P", "Python Atlanta", True),
    ("discord.gg/ccyrDKv", "C#", True),
]

domain_name_blacklist = [
    ("pornhub.com", None, False),
    ("liveleak.com", None, False),
    ("grabify.link", None, False),
    ("bmwforum.co", None, False),
    ("leancoding.co", None, False),
    ("spottyfly.com", None, False),
    ("stopify.co", None, False),
    ("yoütu.be", None, False),
    ("discörd.com", None, False),
    ("minecräft.com", None, False),
    ("freegiftcards.co", None, False),
    ("disçordapp.com", None, False),
    ("fortnight.space", None, False),
    ("fortnitechat.site", None, False),
    ("joinmy.site", None, False),
    ("curiouscat.club", None, False),
    ("catsnthings.fun", None, False),
    ("yourtube.site", None, False),
    ("youtubeshort.watch", None, False),
    ("catsnthing.com", None, False),
    ("youtubeshort.pro", None, False),
    ("canadianlumberjacks.online", None, False),
    ("poweredbydialup.club", None, False),
    ("poweredbydialup.online", None, False),
    ("poweredbysecurity.org", None, False),
    ("poweredbysecurity.online", None, False),
    ("ssteam.site", None, False),
    ("steamwalletgift.com", None, False),
    ("discord.gift", None, False),
    ("lmgtfy.com", None, False),
]

filter_token_blacklist = [
    ("\bgoo+ks*\b", None, False),
    ("\bky+s+\b", None, False),
    ("\bki+ke+s*\b", None, False),
    ("\bbeaner+s?\b", None, False),
    ("\bcoo+ns*\b", None, False),
    ("\bnig+lets*\b", None, False),
    ("\bslant-eyes*\b", None, False),
    ("\btowe?l-?head+s*\b", None, False),
    ("\bchi*n+k+s*\b", None, False),
    ("\bspick*s*\b", None, False),
    ("\bkill* +(?:yo)?urself+\b", None, False),
    ("\bjew+s*\b", None, False),
    ("\bsuicide\b", None, False),
    ("\brape\b", None, False),
    ("\b(re+)tar+(d+|t+)(ed)?\b", None, False),
    ("\bta+r+d+\b", None, False),
    ("\bcunts*\b", None, False),
    ("\btrann*y\b", None, False),
    ("\bshemale\b", None, False),
    ("fa+g+s*", None, False),
    ("卐", None, False),
    ("卍", None, False),
    ("࿖", None, False),
    ("࿕", None, False),
    ("࿘", None, False),
    ("࿗", None, False),
    ("cuck(?!oo+)", None, False),
    ("nigg+(?:e*r+|a+h*?|u+h+)s?", None, False),
    ("fag+o+t+s*", None, False),
]

file_format_whitelist = [
    (".3gp", None, True),
    (".3g2", None, True),
    (".avi", None, True),
    (".bmp", None, True),
    (".gif", None, True),
    (".h264", None, True),
    (".jpg", None, True),
    (".jpeg", None, True),
    (".m4v", None, True),
    (".mkv", None, True),
    (".mov", None, True),
    (".mp4", None, True),
    (".mpeg", None, True),
    (".mpg", None, True),
    (".png", None, True),
    (".tiff", None, True),
    (".wmv", None, True),
    (".svg", None, True),
    (".psd", "Photoshop", True),
    (".ai", "Illustrator", True),
    (".aep", "After Effects", True),
    (".xcf", "GIMP", True),
    (".mp3", None, True),
    (".wav", None, True),
    (".ogg", None, True),
    (".webm", None, True),
    (".webp", None, True),
]

populate_data = {
    "FILTER_TOKEN": filter_token_blacklist,
    "DOMAIN_NAME": domain_name_blacklist,
    "FILE_FORMAT": file_format_whitelist,
    "GUILD_INVITE": guild_invite_whitelist,
}


class Migration(migrations.Migration):
    dependencies = [("api", "0058_create_new_filterlist_model")]

    def populate_filterlists(app, _):
        FilterList = app.get_model("api", "FilterList")

        for filterlist_type, metadata in populate_data.items():
            for content, comment, allowed in metadata:
                FilterList.objects.create(
                    type=filterlist_type,
                    allowed=allowed,
                    content=content,
                    comment=comment,
                )

    def clear_filterlists(app, _):
        FilterList = app.get_model("api", "FilterList")
        FilterList.objects.all().delete()

    operations = [
        migrations.RunPython(populate_filterlists, clear_filterlists)
    ]
