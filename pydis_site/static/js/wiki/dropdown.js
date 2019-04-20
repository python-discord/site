(function() {
    window.dropdowns = {};

    let elements = document.getElementsByClassName("dropdown");

    for (let element of elements) {
        let menu_element = element.getElementsByClassName("dropdown-menu")[0];

        function show() {
            $(element).addClass("is-active");
        }

        function hide() {
            $(element).removeClass("is-active");
        }

        function handle_event(e) {
            show();

            $(document.body).on("click." + menu_element.id, function() {
                hide();

                $(document.body).off("click." + menu_element.id);
            });

            e.stopPropagation();
        }

        $(element).click(handle_event);
        $(element).hover(handle_event);
        $(element).mouseleave(hide);

        window.dropdowns[menu_element.id] = element;
    }
})();
