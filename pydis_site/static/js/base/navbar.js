"use strict";

const defaultCssElement = $("#bulma-css")[0];
const darkCssElement = $("#bulma-css-dark")[0];

function getCurrentTheme() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('theme='))
        .split('=')[1];
}

function displayThemedElements() {
    const defaultElements = Array.from($(".show-default-mode"));
    const darkElements = Array.from($(".show-dark-mode"));

    switch (getCurrentTheme()) {
        case "":
        case "default":
            defaultElements.forEach(e => e.style.display = null);
            darkElements.forEach(e => e.style.display = 'none');
            break;
        case "dark":
            defaultElements.forEach(e => e.style.display = 'none');
            darkElements.forEach(e => e.style.display = null);
            break;
    }
}

function setStyleSheets() {
    switch (getCurrentTheme()) {
        case "":
        case "default":
            defaultCssElement.disabled = false;
            darkCssElement.disabled = true;
            break;
        case "dark":
            defaultCssElement.disabled = true;
            darkCssElement.disabled = false;
            break;
    }
}


// Executed when the page has finished loading.
document.addEventListener("DOMContentLoaded", () => {

    setStyleSheets();
    displayThemedElements();

    $('#theme-switch').on("click", () => {

        // Update cookie
        if (getCurrentTheme() === "dark") {
            document.cookie = "theme=default";
        } else {
            document.cookie = "theme=dark";
        }

        setStyleSheets();
        displayThemedElements();

        // Animations
        let switchToggle = $(".switch")[0];
        let knob = $(".knob")[0];

        if (knob.classList.contains("dark")) {
            knob.classList.remove("dark");
            knob.classList.add("light");

            // After 500ms, switch the icons
            setTimeout(function() {
                switchToggle.classList.remove("dark");
                switchToggle.classList.add("light");
            }, 100);
        } else {
            knob.classList.remove("light");
            knob.classList.add("dark");

            // After 500ms, switch the icons
            setTimeout(function() {
                switchToggle.classList.remove("light");
                switchToggle.classList.add("dark");
            }, 100);
        }
    });
});