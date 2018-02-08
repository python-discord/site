# coding=utf-8
from flask import redirect

from pysite.base_route import RouteView


__author__ = "Gareth Coles"


class InviteView(RouteView):
    path = "/invite"
    name = "invite"

    def get(self):
        return redirect("http://invite.pythondiscord.com/")
