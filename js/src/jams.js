"use strict";

/* exported JamActions */

class JamActions {
    constructor(url, csrf_token) {
        this.url = url;
        this.csrf_token = csrf_token;
    }

    send(action, method, data, callback) {
        data["action"] = action;

        $.ajax(this.url, {
            "data": data,
            "dataType": "json",
            "headers": {"X-CSRFToken": this.csrf_token},
            "method": method,
        }).done(data => {
            if ("error_code" in data) {
                return callback(false, data);
            }

            return callback(true, data);
        }).fail(() => callback(false));
    }

    send_json(action, method, data, callback) {
        data["action"] = action;

        $.ajax(this.url, {
            "data": JSON.stringify(data),
            "dataType": "json",
            "headers": {"X-CSRFToken": this.csrf_token},
            "contentType": "application/json",
            "method": method
        }).done(data => {
            if ("error_code" in data) {
                return callback(false, data);
            }

            return callback(true, data);
        }).fail(() => callback(false));
    }

    set_state(jam, state, callback) {
        this.send(
            "state",
            "POST",
            {
                "jam": jam,
                "state": state
            },
            callback
        );
    }

    get_questions(callback) {
        this.send(
            "questions",
            "GET",
            {},
            callback
        );
    }

    create_question(data, callback) {
        this.send_json(
            "questions",
            "POST",
            data,
            callback
        );
    }

    delete_question(id, callback) {
        this.send(
            "question",
            "DELETE",
            {"id": id},
            callback
        );
    }

    associate_question(form, question, callback) {
        this.send(
            "associate_question",
            "POST",
            {
                "form": form,
                "question": question,
            },
            callback
        );
    }

    disassociate_question(form, question, callback) {
        this.send(
            "disassociate_question",
            "POST",
            {
                "form": form,
                "question": question,
            },
            callback
        );
    }

    create_infraction(id, reason, number, callback) {
        this.send(
            "infraction",
            "POST",
            {
                "participant": id,
                "reason": reason,
                "number": number
            },
            callback
        );
    }

    delete_infraction(id, callback) {
        this.send(
            "infraction",
            "DELETE",
            {"id": id},
            callback
        );
    }

    approve_application(id, callback) {
        this.send(
            "approve_application",
            "POST",
            {"id": id},
            callback
        );
    }

    unapprove_application(id, callback) {
        this.send(
            "unapprove_application",
            "POST",
            {"id": id},
            callback
        );
    }

    generate_teams(jam, callback) {
        this.send(
            "generate_teams",
            "POST",
            {"jam": jam},
            callback
        );
    }

    create_team(jam, callback) {
        this.send(
            "create_team",
            "POST",
            {"jam": jam},
            callback
        );
    }

    reroll_team(team, callback) {
        this.send(
            "reroll_team",
            "POST",
            {"team": team},
            callback
        );
    }

    delete_team(team, callback) {
        this.send(
            "team",
            "DELETE",
            {"team": team},
            callback
        );
    }

    set_team_member(jam, member, team, callback) {
        this.send(
            "set_team_member",
            "POST",
            {"jam": jam, "member": member, "team": team},
            callback
        );
    }

    set_winning_team(team, callback) {
        this.send(
            "set_winning_team",
            "POST",
            {"team": team},
            callback
        );
    }

    unset_winning_team(jam, callback) {
        this.send(
            "unset_winning_team",
            "POST",
            {"jam": jam},
            callback
        );
    }
}
