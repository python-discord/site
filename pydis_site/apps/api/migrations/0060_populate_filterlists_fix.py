from django.db import migrations

bad_guild_invite_whitelist = [
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

guild_invite_whitelist = [
    ("267624335836053506", "Python Discord", True),
    ("348658686962696195", "RLBot", True),
    ("423249981340778496", "Kivy", True),
    ("438622377094414346", "Pyglet", True),
    ("524691714909274162", "Panda3D", True),
    ("666560367173828639", "PyWeek", True),
    ("702724176489873509", "Microsoft Python", True),
    ("222078108977594368", "Discord.js Official", True),
    ("238666723824238602", "Programming Discussions", True),
    ("433980600391696384", "JetBrains Community", True),
    ("204621105720328193", "Raspberry Pie", True),
    ("286633898581164032", "Ren'Py", True),
    ("440186186024222721", "Python Discord: Emojis 1", True),
    ("578587418123304970", "Python Discord: Emojis 2", True),
    ("159039020565790721", "Django", True),
    ("273944235143593984", "STEM", True),
    ("336642139381301249", "discord.py", True),
    ("244230771232079873", "Programmers Hangout", True),
    ("239433591950540801", "SpeakJS", True),
    ("280033776820813825", "Functional Programming", True),
    ("349505959032389632", "PyGame", True),
    ("488751051629920277", "Python Atlanta", True),
    ("143867839282020352", "C#", True),
]


class Migration(migrations.Migration):
    dependencies = [("api", "0059_populate_filterlists")]

    def fix_filterlist(app, _):
        FilterList = app.get_model("api", "FilterList")
        FilterList.objects.filter(type="GUILD_INVITE").delete()  # Clear out the stuff added in 0059.

        for content, comment, allowed in guild_invite_whitelist:
            FilterList.objects.create(
                type="GUILD_INVITE",
                allowed=allowed,
                content=content,
                comment=comment,
            )

    def restore_bad_filterlist(app, _):
        FilterList = app.get_model("api", "FilterList")
        FilterList.objects.filter(type="GUILD_INVITE").delete()

        for content, comment, allowed in bad_guild_invite_whitelist:
            FilterList.objects.create(
                type="GUILD_INVITE",
                allowed=allowed,
                content=content,
                comment=comment,
            )

    operations = [
        migrations.RunPython(fix_filterlist, restore_bad_filterlist)
    ]
