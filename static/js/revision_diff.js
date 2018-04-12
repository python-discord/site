let buttons = document.querySelectorAll("td input");
let id_reg = /compare-(before|after)-([\w|-]+)/;

function getRevisionId(element){
    let e = element.id.match(id_reg);
    return [e[1], e[2]];
}

function getRevision(id) {
    let e = revisions.filter((x) => {
        return x.id === id;
    });
    return e[0];
}

function radioButtonChecked(element) {
    console.log("change detected");
    let id = getRevisionId(element);
    let rev = getRevision(id[1]);
    if (id[0] === "after"){
        document.querySelector(`#compare-before-${id[1]}`).checked = false;

        buttons.forEach(function(e){
            if (getRevisionId(e)[0] === "after" && e.id !== element.id) {
                e.checked = false;
            }


        })
    } else {
        document.querySelector(`#compare-after-${id[1]}`).checked = false;
        buttons.forEach(function(e){
            if (getRevisionId(e)[0] === "before" && e.id !== element.id) {
                e.checked = false;
            }

            if (getRevisionId(e)[0] === "after") {
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

    buttons.forEach((button) => {
        let id = getRevisionId(button);
        if (button.checked && id[0] === "before") {
            bef = id[1];
        }

        if (button.checked && id[0] === "after") {
            aft = id[1];
        }
    })

    document.getElementById("compare-submit").href = `/history/compare/${bef}/${aft}`

}

buttons.forEach(function(button){
    button.checked = false; // Some browsers remember if a button is checked.
    button.onchange = function() {
        radioButtonChecked(button);
    }
});