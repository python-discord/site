from flask import jsonify, request
from rethinkdb import ReqlNonExistenceError

from pysite.base_route import APIView
from pysite.constants import ALL_STAFF_ROLES, BotEventTypes, CHANNEL_JAM_LOGS, ErrorCodes, JAMMERS_ROLE
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin, RMQMixin
from pysite.utils.words import get_word_pairs

GET_ACTIONS = ("questions",)
POST_ACTIONS = (
    "associate_question", "disassociate_question", "infraction", "questions", "state", "approve_application",
    "unapprove_application", "create_team", "generate_teams", "set_team_member",
    "reroll_team"
)
DELETE_ACTIONS = ("infraction", "question", "team")

KEYS = ("action",)
QUESTION_KEYS = ("optional", "title", "type")


class ActionView(APIView, DBMixin, RMQMixin):
    path = "/jams/action"
    name = "jams.action"

    table_name = "code_jams"
    forms_table = "code_jam_forms"
    infractions_table = "code_jam_infractions"
    questions_table = "code_jam_questions"
    responses_table = "code_jam_responses"
    teams_table = "code_jam_teams"
    users_table = "users"

    @csrf
    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        action = request.args.get("action")

        if action not in GET_ACTIONS:
            return self.error(ErrorCodes.incorrect_parameters)

        if action == "questions":
            questions = self.db.get_all(self.questions_table)

            return jsonify({"questions": questions})

    @csrf
    @require_roles(*ALL_STAFF_ROLES)
    def post(self):
        if request.is_json:
            data = request.get_json(force=True)
            action = data["action"] if "action" in data else None
        else:
            action = request.form.get("action")

        if action not in POST_ACTIONS:
            return self.error(ErrorCodes.incorrect_parameters)

        if action == "associate_question":
            form = int(request.form.get("form"))
            question = request.form.get("question")

            form_obj = self.db.get(self.forms_table, form)

            if not form_obj:
                return self.error(ErrorCodes.incorrect_parameters, f"Unknown form: {form}")

            question_obj = self.db.get(self.questions_table, question)

            if not question_obj:
                return self.error(ErrorCodes.incorrect_parameters, f"Unknown question: {question}")

            if question_obj["id"] not in form_obj["questions"]:
                form_obj["questions"].append(question_obj["id"])
                self.db.insert(self.forms_table, form_obj, conflict="replace")

                return jsonify({"question": question_obj})
            else:
                return self.error(
                    ErrorCodes.incorrect_parameters,
                    f"Question {question} already associated with form {form}"
                )

        if action == "disassociate_question":
            form = int(request.form.get("form"))
            question = request.form.get("question")

            form_obj = self.db.get(self.forms_table, form)

            if not form_obj:
                return self.error(ErrorCodes.incorrect_parameters, f"Unknown form: {form}")

            question_obj = self.db.get(self.questions_table, question)

            if not question_obj:
                return self.error(ErrorCodes.incorrect_parameters, f"Unknown question: {question}")

            if question_obj["id"] in form_obj["questions"]:
                form_obj["questions"].remove(question_obj["id"])
                self.db.insert(self.forms_table, form_obj, conflict="replace")

                return jsonify({"question": question_obj})
            else:
                return self.error(
                    ErrorCodes.incorrect_parameters,
                    f"Question {question} not already associated with form {form}"
                )

        if action == "state":
            jam = int(request.form.get("jam"))
            state = request.form.get("state")

            if not all((jam, state)):
                return self.error(ErrorCodes.incorrect_parameters)

            jam_obj = self.db.get(self.table_name, jam)
            jam_obj["state"] = state
            self.db.insert(self.table_name, jam_obj, conflict="update")

            return jsonify({})

        if action == "questions":
            data = request.get_json(force=True)

            for key in QUESTION_KEYS:
                if key not in data:
                    return self.error(ErrorCodes.incorrect_parameters, f"Missing key: {key}")

            title = data["title"]
            optional = data["optional"]
            question_type = data["type"]
            question_data = data.get("data", {})

            if question_type in ["number", "range", "slider"]:
                if "max" not in question_data or "min" not in question_data:
                    return self.error(
                        ErrorCodes.incorrect_parameters, f"{question_type} questions must have both max and min values"
                    )

                result = self.db.insert(
                    self.questions_table,
                    {
                        "title": title,
                        "optional": optional,
                        "type": question_type,
                        "data": {
                            "max": question_data["max"],
                            "min": question_data["min"]
                        }
                    },
                    conflict="error"
                )
            elif question_type == "radio":
                if "options" not in question_data:
                    return self.error(
                        ErrorCodes.incorrect_parameters, f"{question_type} questions must have both options"
                    )

                result = self.db.insert(
                    self.questions_table,
                    {
                        "title": title,
                        "optional": optional,
                        "type": question_type,
                        "data": {
                            "options": question_data["options"]
                        }
                    },
                    conflict="error"
                )
            else:
                result = self.db.insert(
                    self.questions_table,
                    {  # No extra data for other types of question
                        "title": title,
                        "optional": optional,
                        "type": question_type
                    },
                    conflict="error"
                )

            return jsonify({"id": result["generated_keys"][0]})

        if action == "infraction":
            participant = request.form.get("participant")
            reason = request.form.get("reason")

            if not participant or not reason or "number" not in request.form:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Infractions must have a participant, reason and number"
                )

            number = int(request.form.get("number"))

            result = self.db.insert(self.infractions_table, {
                "participant": participant,
                "reason": reason,
                "number": number,
                "decremented_for": []
            })

            return jsonify({"id": result["generated_keys"][0]})

        if action == "create_team":
            jam = request.form.get("jam", type=int)

            if not jam:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Jam number required"
                )

            jam_data = self.db.get(self.table_name, jam)

            if not jam_data:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Unknown jam number"
                )

            word_pairs = get_word_pairs()
            adjective, noun = list(word_pairs)[0]

            team = {
                "name": f"{adjective} {noun}".title(),
                "members": []
            }

            result = self.db.insert(self.teams_table, team)
            team["id"] = result["generated_keys"][0]

            jam_obj = self.db.get(self.table_name, jam)
            jam_obj["teams"].append(team["id"])

            self.db.insert(self.table_name, jam_obj, conflict="replace")

            return jsonify({"team": team})

        if action == "generate_teams":
            jam = request.form.get("jam", type=int)

            if not jam:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Jam number required"
                )

            try:
                query = self.db.query(self.table_name).get(jam).merge(
                    lambda jam_obj: {
                        "participants":
                            self.db.query(self.responses_table)
                                .filter({"jam": jam_obj["number"], "approved": True})
                                .eq_join("snowflake", self.db.query(self.users_table))
                                .without({"left": ["snowflake", "answers"]})
                                .zip()
                                .order_by("username")
                                .coerce_to("array"),
                        "teams":
                            self.db.query(self.teams_table)
                                .outer_join(self.db.query(self.table_name),
                                            lambda team_row, jams_row: jams_row["teams"].contains(team_row["id"]))
                                .pluck({"left": ["id", "name", "members"]})
                                .zip()
                                .coerce_to("array")
                    }
                )

                jam_data = self.db.run(query)
            except ReqlNonExistenceError:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Unknown jam number"
                )

            if jam_data["teams"]:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Jam already has teams"
                )

            num_participants = len(jam_data["participants"])
            num_teams = num_participants // 3

            if num_participants % 3:
                num_teams += 1

            word_pairs = get_word_pairs(num_teams)
            teams = []

            for adjective, noun in word_pairs:
                team = {
                    "name": f"{adjective} {noun}".title(),
                    "members": []
                }

                result = self.db.insert(self.teams_table, team, durability="soft")
                team["id"] = result["generated_keys"][0]
                teams.append(team)

            self.db.sync(self.teams_table)

            jam_obj = self.db.get(self.table_name, jam)
            jam_obj["teams"] = [team["id"] for team in teams]

            self.db.insert(self.table_name, jam_obj, conflict="replace")

            return jsonify({"teams": teams})

        if action == "set_team_member":
            jam = request.form.get("jam", type=int)
            member = request.form.get("member")
            team = request.form.get("team")

            if not jam:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Jam number required"
                )

            if not member:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Member ID required"
                )

            if not team:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Team ID required"
                )

            try:
                query = self.db.query(self.table_name).get(jam).merge(
                    lambda jam_obj: {
                        "participants":
                            self.db.query(self.responses_table)
                                .filter({"jam": jam_obj["number"], "approved": True})
                                .eq_join("snowflake", self.db.query(self.users_table))
                                .without({"left": ["snowflake", "answers"]})
                                .zip()
                                .order_by("username")
                                .coerce_to("array"),
                        "teams":
                            self.db.query(self.teams_table)
                                .outer_join(self.db.query(self.table_name),
                                            lambda team_row, jams_row: jams_row["teams"].contains(team_row["id"]))
                                .pluck({"left": ["id", "name", "members"]})
                                .zip()
                                .coerce_to("array")
                    }
                )

                jam_data = self.db.run(query)
            except ReqlNonExistenceError:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Unknown jam number"
                )

            if not jam_data["teams"]:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Jam has no teams"
                )

            team_obj = self.db.get(self.teams_table, team)

            if not team_obj:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Unknown team ID"
                )

            for jam_team_obj in jam_data["teams"]:
                if jam_team_obj["id"] == team:
                    if member not in jam_team_obj["members"]:
                        jam_team_obj["members"].append(member)

                        self.db.insert(self.teams_table, jam_team_obj, conflict="replace")
                else:
                    if member in jam_team_obj["members"]:
                        jam_team_obj["members"].remove(member)

                        self.db.insert(self.teams_table, jam_team_obj, conflict="replace")

            return jsonify({"result": True})

        if action == "reroll_team":
            team = request.form.get("team")

            if not team:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Team ID required"
                )

            team_obj = self.db.get(self.teams_table, team)

            if not team_obj:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Unknown team ID"
                )

            word_pairs = get_word_pairs()
            adjective, noun = list(word_pairs)[0]

            team_obj["name"] = f"{adjective} {noun}".title()

            self.db.insert(self.teams_table, team_obj, conflict="replace")

            return jsonify({"name": team_obj["name"]})

        if action == "approve_application":
            app = request.form.get("id")

            if not app:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Application ID required"
                )

            app_obj = self.db.get(self.responses_table, app)

            if not app_obj:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Unknown application ID"
                )

            app_obj["approved"] = True

            self.db.insert(self.responses_table, app_obj, conflict="replace")

            jam_obj = self.db.get(self.table_name, app_obj["jam"])

            snowflake = app_obj["snowflake"]
            participants = jam_obj.get("participants", [])

            if snowflake not in participants:
                participants.append(snowflake)
                jam_obj["participants"] = participants
                self.db.insert(self.table_name, jam_obj, conflict="replace")

            self.rmq_bot_event(
                BotEventTypes.add_role,
                {
                    "reason": "Code jam application approved",
                    "role_id": JAMMERS_ROLE,
                    "target": snowflake,
                }
            )

            self.rmq_bot_event(
                BotEventTypes.send_message,
                {
                    "message": f"Congratulations <@{snowflake}> - you've been approved, "
                               f"and we've assigned you the Jammer role!",
                    "target": CHANNEL_JAM_LOGS,
                }
            )

            return jsonify({"result": "success"})

        if action == "unapprove_application":
            app = request.form.get("id")

            if not app:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Application ID required"
                )

            app_obj = self.db.get(self.responses_table, app)

            if not app_obj:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Unknown application ID"
                )

            app_obj["approved"] = False

            self.db.insert(self.responses_table, app_obj, conflict="replace")

            jam_obj = self.db.get(self.table_name, app_obj["jam"])

            snowflake = app_obj["snowflake"]
            participants = jam_obj.get("participants", [])

            if snowflake in participants:
                participants.remove(snowflake)
                jam_obj["participants"] = participants

                self.db.insert(self.table_name, jam_obj, conflict="replace")

            self.rmq_bot_event(
                BotEventTypes.remove_role,
                {
                    "reason": "Code jam application unapproved",
                    "role_id": JAMMERS_ROLE,
                    "target": snowflake,
                }
            )

            return jsonify({"result": "success"})

    @csrf
    @require_roles(*ALL_STAFF_ROLES)
    def delete(self):
        action = request.form.get("action")

        if action not in DELETE_ACTIONS:
            return self.error(ErrorCodes.incorrect_parameters)

        if action == "question":
            question = request.form.get("id")

            if not question:
                return self.error(ErrorCodes.incorrect_parameters, f"Missing key: id")

            question_obj = self.db.get(self.questions_table, question)

            if not question_obj:
                return self.error(ErrorCodes.incorrect_parameters, f"Unknown question: {question}")

            self.db.delete(self.questions_table, question)

            for form_obj in self.db.get_all(self.forms_table):
                if question in form_obj["questions"]:
                    form_obj["questions"].remove(question)
                    self.db.insert(self.forms_table, form_obj, conflict="replace")

            return jsonify({"id": question})

        if action == "infraction":
            infraction = request.form.get("id")

            if not infraction:
                return self.error(ErrorCodes.incorrect_parameters, "Missing key id")

            infraction_obj = self.db.get(self.infractions_table, infraction)

            if not infraction_obj:
                return self.error(ErrorCodes.incorrect_parameters, f"Unknown infraction: {infraction}")

            self.db.delete(self.infractions_table, infraction)

            return jsonify({"id": infraction_obj["id"]})

        if action == "team":
            team = request.form.get("team")

            if not team:
                return self.error(
                    ErrorCodes.incorrect_parameters, "Team ID required"
                )

            self.db.delete(self.teams_table, team)

            return jsonify({"result": True})
