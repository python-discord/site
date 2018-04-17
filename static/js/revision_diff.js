"use strict";

(function() {
let buttons = document.querySelectorAll("td input"); // Fetch all radio buttons
let id_reg = /compare-(before|after)-([\w|-]+)/; // Matches compare-after/before-ID


function getRevisionId(element
    let e = element.id.match(id_reg); // Match ID with RegExp
    return [e[1], e[2]]; // e is in format of [full id, after/before, ID] we only want ID & mode
}

function getRevision(id) {
    let e = revisions.filter((x) => {
        return x.id === id; // Filter through all revisions to find the selected one (revisions in declared in the template)
    });
    return e[0];
}

function radioButtonChecked(element) {
    console.log("change detected");
    let id = getRevisionId(element);
    let rev = getRevision(id[1]);
    if (id[0] === "after"){
        document.querySelector(`#compare-before-${id[1]}`).checked = false; // Deselect the opposite checkbox to the one which has been checked
                                                                            // because we don't want checking of the same revision

        buttons.forEach(function(e){
            if (getRevisionId(e)[0] === "after" && e.id !== element.id) {  // Deselect all checkboxes in the same row
                e.checked = false;
            }
        })
    } else { // This else does the same as above but for the before column
        document.querySelector(`#compare-after-${id[1]}`).checked = false;
        buttons.forEach(function(e){
            if (getRevisionId(e)[0] === "before" && e.id !== element.id) {
                e.checked = false;
            }

            if (getRevisionId(e)[0] === "after") { // This makes sure that you do not compare a new revision with an old one
                let tmprev = getRevision(getRevisionId(e)[1])
                console.log(tmprev);
                if (tmprev.date <= rev.date) {
                    document.querySelector(`#${e.id}`).setAttribute("disabled", "")
                } else {
                    document.querySelector(`#${e.id}`).removeAttribute("disabled")
                }
            }
        });
    }

    let bef, aft;

    buttons.forEach((button) => { // Find the selected posts
        let id = getRevisionId(button);
        if (button.checked && id[0] === "before") {
            bef = id[1];
        }

        if (button.checked && id[0] === "after") {
            aft = id[1];
        }
    })

    document.getElementById("compare-submit").href = `/history/compare/${bef}/${aft}` // Switch the buttons HREF to point to the correct compare URL

}

buttons.forEach(function(button){
    button.checked = false; // Some browsers remember if a button is checked.
    button.onchange = function() {
        radioButtonChecked(button);
    }
});
})();
