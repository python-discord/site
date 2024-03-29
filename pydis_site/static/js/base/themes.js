"use strict";

const defaultTheme = "light";
const stylesheet = document.getElementById("bulma-css");
const htmlTag = document.querySelector("html");

// We include the dark stylesheet in base template to include the rel="preload",
// but remove the actual rel="stylesheet" element here because we won't need it.
document.getElementById("bulma-css-dark").remove();

// Get saved preference for the site in local storage, optionally accounting
// for system preference used when a page loads.
function getCurrentTheme(systemPrefers) {
    const theme = localStorage.getItem("theme");

    if (theme !== null && theme !== "")
        return theme;

    if (systemPrefers !== undefined)
        return systemPrefers;

    return defaultTheme;
}

// Disable & enable the correct CSS stylesheets based on chosen theme.
function setStyleSheets(newTheme) {
    switch (newTheme) {
        case "light":
            stylesheet.href = "/static/css/bulma.css";
            break;
        case "dark":
            stylesheet.href = "/static/css/dark_bulma.css";
            break;
    }

    htmlTag.setAttribute("data-theme", newTheme);
}

// Reflect chosen theme on the switch toggle.
function toggleThemeSwitch(newTheme) {
    const switchToggle = document.getElementById("theme-switch");
    const knob = document.getElementById("theme-knob");

    switch (newTheme) {
        case "light":
            knob.classList.remove("dark");
            knob.classList.add("light");
            setTimeout(function() {
                switchToggle.classList.remove("dark");
                switchToggle.classList.add("light");
            }, 100);
            break;
        case "dark":
            knob.classList.remove("light");
            knob.classList.add("dark");
            setTimeout(function() {
                switchToggle.classList.remove("light");
                switchToggle.classList.add("dark");
            }, 100);
            break;
    }
}

let theme;
const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)");

if (systemPrefersDark.matches)
    theme = getCurrentTheme("dark");
else
    theme = getCurrentTheme();

setStyleSheets(theme);

// Executed when the page has finished loading.
document.addEventListener("DOMContentLoaded", () => {
    toggleThemeSwitch(theme);

    systemPrefersDark.addEventListener("change", ({matches: isDark}) => {
        const newTheme = isDark ? "dark" : "light";
        // Let the new system preference take precedence over toggle preference
        // on page reloads.
        localStorage.removeItem("theme");
        setStyleSheets(newTheme);
        toggleThemeSwitch(newTheme);
    })

    const switchToggle = document.getElementById("theme-switch");
    switchToggle.addEventListener("click", () => {
        const newTheme = htmlTag.getAttribute("data-theme") === "light" ? "dark" : "light";
        localStorage.setItem("theme", newTheme);
        setStyleSheets(newTheme);
        toggleThemeSwitch(newTheme);
    });
});
