"use strict";

/* exported wiki_sidebar */

function wiki_sidebar(){
    const visible_class = "uk-visible@s";
    const sidebar = document.getElementById("wiki-sidebar");
    const display_button = document.getElementById("wiki-sidebar-button");

    display_button.onclick = function() {
        if (sidebar.classList.contains(visible_class)) {
            sidebar.classList.remove(visible_class);
        } else {
            sidebar.classList.add(visible_class);
        }
    };
}
