# coding=utf-8


class Index:
    path = ["/invite"]

    def get(self, res):
        return res.Response(
            status_code=301, text="http://invite.pythondiscord.com/")
