function open_modal(id) {
    let element = document.getElementById(id);

    $(element).addClass("is-active");

    $(element).find(".modal-background").click(function() {
        $(element).removeClass("is-active");
    });

    $(element).find("[aria-label=\"close\"]").click(function(e) {
        $(element).removeClass("is-active");
        e.preventDefault();
    });
}
