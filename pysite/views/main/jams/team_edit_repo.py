import logging
import re
from urllib.parse import quote

import requests
from flask import jsonify, request
from rethinkdb import ReqlNonExistenceError
from urllib3.util import parse_url
from werkzeug.exceptions import NotFound, Unauthorized

from pysite.base_route import APIView
from pysite.constants import ErrorCodes, GITLAB_ACCESS_TOKEN
from pysite.decorators import csrf
from pysite.mixins import DBMixin, OAuthMixin

log = logging.getLogger(__name__)


class JamsTeamEditRepo(APIView, DBMixin, OAuthMixin):
    path = "/jams/teams/<string:team_id>/edit_repo"
    name = "jams.team.edit_repo"

    table_name = "code_jam_teams"
    jams_table = "code_jams"

    gitlab_projects_api_endpoint = "https://gitlab.com/api/v4/projects/{0}"

    @csrf
    def post(self, team_id):
        if not self.user_data:
            return self.redirect_login()

        try:
            query = self.db.query(self.table_name).get(team_id).merge(
                lambda team: {
                    "jam":
                        self.db.query("code_jams").filter(
                            lambda jam: jam["teams"].contains(team["id"])
                        ).coerce_to("array")[0]
                }
            )

            team = self.db.run(query)
        except ReqlNonExistenceError:
            log.exception("Failed RethinkDB query")
            raise NotFound()

        # Only team members can use this route
        if not self.user_data["user_id"] in team["members"]:
            raise Unauthorized()

        repo_url = request.form.get("repo_url").strip()

        # Check if repo is a valid GitLab repo URI
        url = parse_url(repo_url)

        if url.host != "gitlab.com" or url.path is None:
            return self.error(
                ErrorCodes.incorrect_parameters,
                "Not a GitLab repository."
            )

        project_path = url.path.strip("/")  # /user/repository/ --> user/repository
        if len(project_path.split("/")) < 2:
            return self.error(
                ErrorCodes.incorrect_parameters,
                "Not a valid repository."
            )

        word_regex = re.compile("^[\-\.\w]+$")  # Alphanumerical, underscores, periods, and dashes
        for segment in project_path.split("/"):
            if not word_regex.fullmatch(segment):
                return self.error(
                    ErrorCodes.incorrect_parameters,
                    "Not a valid repository."
                )

        project_path_encoded = quote(project_path, safe='')  # Replaces / with %2F, etc.

        # If validation returns something else than True, abort
        validation = self.validate_project(team, project_path_encoded)
        if validation is not True:
            return validation

        # Update the team repo
        # Note: the team repo is only stored using its path (e.g. user/repository)
        team_obj = self.db.get(self.table_name, team_id)
        team_obj["repo"] = project_path
        self.db.insert(self.table_name, team_obj, conflict="update")

        return jsonify(
            {
                "project_path": project_path
            }
        )

    def validate_project(self, team, project_path):
        # Check on GitLab if the project exists
        # NB: certain fields (such as "forked_from_project") need an access token
        # to be visible. Set the GITLAB_ACCESS_TOKEN env variable to solve this
        query_response = self.request_project(project_path)

        if query_response.status_code != 200:
            return self.error(
                ErrorCodes.incorrect_parameters,
                "Not a valid repository."
            )

        # Check if the jam's base repo has been set by staff
        # If not, just ignore the fork check and proceed
        if "repo" not in team["jam"]:
            return True
        jam_repo = team["jam"]["repo"]

        # Check if the provided repo is a forked repo
        project_data = query_response.json()
        if "forked_from_project" not in project_data:
            return self.error(
                ErrorCodes.incorrect_parameters,
                "This repository is not a fork of the jam's repository."
            )

        # Check if the provided repo is forking the base repo
        forked_from_project = project_data["forked_from_project"]

        # The jam repo is stored in full (e.g. https://gitlab.com/user/repository)
        jam_repo_path = quote(parse_url(jam_repo).path.strip("/"), safe='')

        # Get info about the code jam repo
        jam_repo_response = self.request_project(jam_repo_path)

        # Something went wrong, fail silently
        if jam_repo_response.status_code != 200:
            return True

        # Check if the IDs for the code jam repo and the fork source match
        jam_repo_data = jam_repo_response.json()
        if jam_repo_data["id"] != forked_from_project["id"]:
            return self.error(
                ErrorCodes.incorrect_parameters,
                "This repository is not a fork of the jam's repository."
            )

        # All good
        return True

    def request_project(self, project_path):
        # Request the project details using a private access token
        return requests.get(
            self.gitlab_projects_api_endpoint.format(project_path),
            params={
                "private_token": GITLAB_ACCESS_TOKEN
            }
        )
