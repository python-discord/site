from flask import jsonify, request

from pysite.base_route import APIView
from pysite.constants import ALL_STAFF_ROLES, ErrorCodes
from pysite.decorators import csrf, require_roles
from pysite.mixins import DBMixin

GET_ACTIONS = ["questions"]
POST_ACTIONS = ["associate_question", "disassociate_question", "questions", "state"]
KEYS = ["action"]

QUESTION_KEYS = ["optional", "title", "type"]


class ActionView(APIView, DBMixin):
    path = "/jams/action"
    name = "jams.action"

    table_name = "code_jams"
    forms_table = "code_jam_forms"
    questions_table = "code_jam_questions"

    @csrf
    @require_roles(*ALL_STAFF_ROLES)
    def get(self):
        action = request.args.get("action")

        if action not in GET_ACTIONS:
            return self.error(ErrorCodes.incorrect_parameters)

        if action == "questions":
            questions = self.db.get_all(self.questions_table)

            print(questions)
            return jsonify({"questions": questions})

    @csrf
    @require_roles(*ALL_STAFF_ROLES)
    def post(self):
        action = request.args.get("action")

        if action not in POST_ACTIONS:
            return self.error(ErrorCodes.incorrect_parameters)

        if action == "associate_question":
            form = int(request.args.get("form"))
            question = request.args.get("question")

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
            form = int(request.args.get("form"))
            question = request.args.get("question")

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
            jam = int(request.args.get("jam"))
            state = request.args.get("state")

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
