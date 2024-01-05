"use strict";

const defaultTheme = "light";
const lightCssElement = document.getElementById("bulma-css");
const darkCssElement = document.getElementById("bulma-css-dark");

function getCurrentTheme() {
    const theme = localStorage.getItem("theme");
    if (theme === null || theme === "")
        return defaultTheme;
    return theme;
}

function setStyleSheets(newTheme) {
    switch (newTheme) {
        case "light":
            lightCssElement.disabled = false;
            darkCssElement.disabled = true;
            break;
        case "dark":
            lightCssElement.disabled = true;
            darkCssElement.disabled = false;
            break;
    }
}

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

// Executed when the page has finished loading.
document.addEventListener("DOMContentLoaded", () => {
    const theme = getCurrentTheme()
    setStyleSheets(theme);
    toggleThemeSwitch(theme);

    const switchToggle = document.getElementById("theme-switch");
    switchToggle.addEventListener("click", () => {
        const newTheme = getCurrentTheme() === "light" ? "dark" : "light";
        console.log(newTheme);
        localStorage.setItem("theme", newTheme);
        setStyleSheets(newTheme);
        toggleThemeSwitch(newTheme);
    });
});
