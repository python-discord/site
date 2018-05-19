"use strict";

function refreshLock() {
    console.log("Refreshing lock");
    let oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function() {
        let response = JSON.parse(this.responseText);

        if (response.error !== undefined) {
            document.getElementById("submit").disabled = true;

            if (response.error_lines !== undefined) {
                editor.session.setAnnotations(response.error_lines);
                document.getElementById("preview-div").innerHTML ="<h3>Error - see editor margin</h3>";
            } else {
                console.log("Error: " + response.error);
                document.getElementById("preview-div").innerHTML ="<h3>Error</h3><p>" + response.error + "<p>";
            }
        } else {
            document.getElementById("submit").disabled = false;
            document.getElementById("preview-div").innerHTML = response.data;

            editor.session.setAnnotations([]);
        }
    });

    let data = editor.getValue();

    if (data.replace("\s", "").length < 1 || document.getElementById("title").value.length < 1) {
        document.getElementById("submit").disabled = true;
        return false;
    }

    oReq.open("POST", "/render");

    oReq.setRequestHeader("Content-type", "application/json");
    oReq.setRequestHeader("X-CSRFToken", csrf_token);

    oReq.send(JSON.stringify({"data": editor.getValue()}));
}

class Actions {
    constructor(url, csrf_token) {
        this.url = url;
        this.csrf_token = csrf_token;
    }

    send(action, method, data, callback) {
        let oReq = new XMLHttpRequest();

        oReq.addEventListener("load", function() {
            let result;

            try {
                result = JSON.parse(this.responseText);
            } catch (e) {
                return callback(false);
            }

            if ("error_code" in result) {
                return callback(false, result);
            }

            return callback(true, result);
        });

        data["action"] = action;

        let params = this.get_params(data);
        let url = this.url + "?" + params;

        oReq.open(method, url);
        oReq.setRequestHeader("X-CSRFToken", this.csrf_token);
        oReq.send();
    }

    send_json(action, method, data, callback) {
        let oReq = new XMLHttpRequest();

        oReq.addEventListener("load", function() {
            let result;

            try {
                result = JSON.parse(this.responseText);
            } catch (e) {
                return callback(false);
            }

            if ("error_code" in result) {
                return callback(false, result);
            }

            return callback(true, result);
        });

        data = JSON.stringify(data);

        let params = this.get_params({"action": action});
        let url = this.url + "?" + params;

        oReq.open(method, url);
        oReq.setRequestHeader("X-CSRFToken", this.csrf_token);
        oReq.send(data);
    }

    get_params(data) {  // https://stackoverflow.com/a/12040639
        return Object.keys(data).map(function(key) {
            return [key, data[key]].map(encodeURIComponent).join("=");
        }).join("&");
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
        )
    }

    delete_question(id, callback) {
        this.send(
            "question",
            "DELETE",
            {
                "id": id
            },
            callback
        )
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
        )
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
        )
    }
}