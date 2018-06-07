from flask import redirect, request, url_for
from werkzeug.exceptions import BadRequest

from pysite.base_route import RouteView
from pysite.decorators import csrf
from pysite.mixins import DBMixin, OAuthMixin


class JamsProfileView(RouteView, DBMixin, OAuthMixin):
    path = "/jams/profile"
    name = "jams.profile"

    table_name = "code_jam_participants"

    def get(self):
        if not self.user_data:
            return self.redirect_login()

        participant = self.db.get(self.table_name, self.user_data["user_id"])
        existing = True

        if not participant:
            participant = {"id": self.user_data["user_id"]}
            existing = False

        form = request.args.get("form")

        if form:
            try:
                form = int(form)
            except ValueError:
                pass  # Someone trying to have some fun I guess

        return self.render(
            "main/jams/profile.html", participant=participant, form=form, existing=existing
        )

    @csrf
    def post(self):
        if not self.user_data:
            return self.redirect_login()

        participant = self.db.get(self.table_name, self.user_data["user_id"])

        if not participant:
            participant = {"id": self.user_data["user_id"]}

        gitlab_username = request.form.get("gitlab_username")
        timezone = request.form.get("timezone")

        if not gitlab_username or not timezone:
            return BadRequest()

        participant["gitlab_username"] = gitlab_username
        participant["timezone"] = timezone

        self.db.insert(self.table_name, participant, conflict="replace")

        form = request.args.get("form")

        if form:
            try:
                form = int(form)
            except ValueError:
                pass  # Someone trying to have some fun I guess
            else:
                return redirect(url_for("main.jams.join", jam=form))

        return self.render(
            "main/jams/profile.html", participant=participant, done=True, existing=True
        )
