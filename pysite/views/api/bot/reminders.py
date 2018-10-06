from flask import jsonify
from schema import Optional, Schema

from pysite.base_route import APIView
from pysite.constants import ValidationTypes
from pysite.decorators import api_key, api_params
from pysite.mixins import DBMixin
from pysite.utils.time import parse_duration

GET_SCHEMA = Schema({
    Optional("reminder_id"): str
})

POST_SCHEMA = Schema({
    "user_id": str,
    "content": str,
    "duration": str,
    "channel_id": str
})

DELETE_SCHEMA = Schema({
    "reminders": [str]
})

USER_GET_SCHEMA = Schema({
    "user_id": str
})

USER_UPDATE_SCHEMA = Schema({
    "user_id": str,
    "friendly_id": str,
    Optional("duration"): str,
    Optional("content"): str
})

USER_DELETE_SCHEMA = Schema({
    "user_id": str,
    "friendly_id": str
})


class RemindersView(APIView, DBMixin):
    path = '/bot/reminders'
    name = 'bot.reminders'
    table_name = 'reminders'

    @api_key
    @api_params(schema=GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params=None):
        """
        Get a list of all reminders in the database,
        or a specific reminder given its ID.

        API key must be provided as header.
        """

        if params:
            reminder = self.db.get(self.table_name, params["reminder_id"])
            data = {"reminder": reminder}

        else:
            reminders = self.db.get_all(self.table_name)
            data = {"reminders": reminders}

        return jsonify({"success": True, **data})

    @api_key
    @api_params(schema=POST_SCHEMA, validation_type=ValidationTypes.json)
    def post(self, json_data):
        """
        Create and save a new reminder.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        duration = json_data["duration"]

        try:
            remind_at = parse_duration(duration)
        except ValueError:
            return jsonify({
                "success": False,
                "error_message": "An invalid duration was given."
            })

        # Get all of the user's active reminders
        user_id_filter = {"user_id": json_data["user_id"]}
        active_reminders = self.db.run(
            self.db.query(self.table_name)
            .filter(user_id_filter)
        )

        # Find all the friendly ID's that are currently in use for this user.
        taken_ids = (rem["friendly_id"] for rem in active_reminders)

        # Search for the smallest available friendly ID
        friendly_id = 0
        while str(friendly_id) in taken_ids:
            friendly_id += 1

        # Set up the data to be inserted to the table
        reminder_data = {
            "user_id": json_data["user_id"],
            "content": json_data["content"],
            "remind_at": remind_at,
            "channel_id": json_data["channel_id"],
            "friendly_id": str(friendly_id)
        }

        # Insert the data and get the generated ID
        reminder_id = self.db.insert(self.table_name, reminder_data)["generated_keys"][0]

        # Create the JSON response data
        response = {
            "reminder": {
                "id": reminder_id,
                **reminder_data
            }
        }

        return jsonify({"success": True, **response})

    @api_key
    @api_params(schema=DELETE_SCHEMA, validation_type=ValidationTypes.json)
    def delete(self, json_data):
        """
        Delete a list of reminders from the database, given their IDs.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        changes = self.db.run(
            self.db.query(self.table_name)
            .get_all(*json_data["reminders"])
            .delete()
        )

        return jsonify({"success": True, **changes})


class RemindersByUserView(APIView, DBMixin):
    path = "/bot/reminders/user"
    name = "bot.reminders.user"
    table_name = "reminders"

    def _get_full_reminder(self, user_id: str, friendly_id: str):
        """
        Get a user's reminder content.

        :param user_id: The reminder's user.
        :param friendly_id: The user's ID for the reminder.
        :return: The UUID for the reminder.
        """

        filter_data = {
            "user_id": user_id,
            "friendly_id": friendly_id
        }

        reminders = self.db.run(
            self.db.query(self.table_name)
            .filter(filter_data)
            .coerce_to("array")
        )

        if reminders:
            return reminders[0]

        else:
            return None

    @api_key
    @api_params(schema=USER_GET_SCHEMA, validation_type=ValidationTypes.params)
    def get(self, params):
        """
        Get all reminders for a user.

        API key must be provided as header.
        """

        reminders = self.db.run(
            self.db.query(self.table_name)
            .filter({"user_id": params["user_id"]})
            .coerce_to("array")
        )

        return jsonify({"success": True, "reminders": reminders})

    @api_key
    @api_params(schema=USER_UPDATE_SCHEMA, validation_type=ValidationTypes.json)
    def patch(self, json_data):
        """
        Update the duration or content of a user's reminder.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        reminder = self._get_full_reminder(
            json_data["user_id"],
            json_data["friendly_id"]
        )

        if not reminder:
            return jsonify({
                "success": False,
                "error_message": "Reminder could not be found."
            })

        if "duration" in json_data:
            duration = json_data["duration"]

            # Attempt to update the duration, but return if it's invalid.
            try:
                reminder["remind_at"] = parse_duration(duration)
            except ValueError:
                return jsonify({
                    "success": False,
                    "error_message": "An invalid duration was given."
                })

        if "content" in json_data:
            reminder["content"] = json_data["content"]

        # Update the reminder with the new information
        update_result = self.db.run(
            self.db.query(self.table_name)
            .update(reminder)
        )

        # Make sure something actually changed
        if not update_result["replaced"]:
            return jsonify({
                "success": False,
                "error_message": "Nothing was changed."
            })

        return jsonify({"success": True, "reminder": reminder})

    @api_key
    @api_params(schema=USER_DELETE_SCHEMA, validation_type=ValidationTypes.json)
    def delete(self, json_data):
        """
        Delete a user's reminder from the database.

        Data must be provided as JSON.
        API key must be provided as header.
        """

        reminder = self._get_full_reminder(
            json_data["user_id"],
            json_data["friendly_id"]
        )

        if not reminder:
            return jsonify({
                "success": False,
                "error_message": "Reminder could not be found."
            })

        self.db.run(
            self.db.query(self.table_name)
            .get(reminder["id"])
            .delete()
        )

        return jsonify({"success": True, "reminder_id": reminder["id"]})
