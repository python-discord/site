"use strict";

(function() {
    const buttons = document.querySelectorAll("td input"); // Fetch all radio buttons
    const id_reg = /compare-(before|after)-([\w|-]+)/; // Matches compare-after/before-ID


    function getRevisionId(element){
        const e = element.id.match(id_reg); // Match ID with RegExp
        return [e[1], e[2]]; // e is in format of [full id, after/before, ID] we only want ID & mode
    }

    function getRevision(id) {
        /* global revisions */ // TODO: FIXME

        const e = revisions.filter((x) => {
            // Filter through all revisions to find the selected one (revisions in declared in the template)
            return x.id === id;
        });
        return e[0];
    }

    function radioButtonChecked(element) {
        // console.log("change detected");
        const id = getRevisionId(element);
        const rev = getRevision(id[1]);
        if (id[0] === "after"){
            /*
             * Deselect the opposite checkbox to the one which has been checked
             * because we don't want checking of the same revision
             */

            document.querySelector(`#compare-before-${id[1]}`).checked = false;

            buttons.forEach((e) => {
                if (getRevisionId(e)[0] === "after" && e.id !== element.id) { // Deselect all checkboxes in the same row
                    e.checked = false;
                }
            });
        } else { // This else does the same as above but for the before column
            document.querySelector(`#compare-after-${id[1]}`).checked = false;
            buttons.forEach((e) => {
                if (getRevisionId(e)[0] === "before" && e.id !== element.id) {
                    e.checked = false;
                }

                // This makes sure that you do not compare a new revision with an old one
                if (getRevisionId(e)[0] === "after") {
                    const tmprev = getRevision(getRevisionId(e)[1]);
                    // console.log(tmprev);
                    if (tmprev.date <= rev.date) {
                        document.querySelector(`#${e.id}`).setAttribute("disabled", "");
                    } else {
                        document.querySelector(`#${e.id}`).removeAttribute("disabled");
                    }
                }
            });
        }

        let aft, bef;

        buttons.forEach((button) => { // Find the selected posts
            const id = getRevisionId(button);
            if (button.checked && id[0] === "before") {
                bef = id[1];
            }

            if (button.checked && id[0] === "after") {
                aft = id[1];
            }
        });

        // Switch the buttons HREF to point to the correct compare URL
        document.getElementById("compare-submit").href = `/history/compare/${bef}/${aft}`;

    }

    buttons.forEach((button) => {
        button.checked = false; // Some browsers remember if a button is checked.
        button.onchange = function() {
            radioButtonChecked(button);
        };
    });
})();
