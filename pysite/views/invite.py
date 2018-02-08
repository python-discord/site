# coding=utf-8
from flask import redirect

from pysite.base_route import BaseView


class InviteView(BaseView):
    path = "/invite"
    name = "invite"

    def get(self):
        return redirect("http://invite.pythondiscord.com/")
