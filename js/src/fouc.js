"use strict";

function getScript(url, integrity, cross_origin) {
    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src = url;
    script.defer = true;

    if (integrity !== undefined) {
        script.integrity = integrity;
    }

    if (cross_origin !== undefined) {
        script.crossOrigin = cross_origin;
    }

    document.getElementsByTagName("head")[0].appendChild(script);
}

function setClass(selector, my_class) {
    const element = document.querySelector(selector);
    // console.log(element);
    element.className = my_class;
}

function removeClass(selector, my_class) {
    const element = document.querySelector(selector);
    const reg = new RegExp(`(^| )${my_class}($| )`, "g");
    element.className = element.className.replace(reg, " ");
}

// hide the html when the page loads, but only if js is turned on.
setClass("html", "prevent-fouc");

// when the DOM has finished loading, unhide the html
document.onreadystatechange = function () {
    if (document.readyState === "interactive") {
        removeClass("html", "prevent-fouc");
        getScript(
            "https://pro.fontawesome.com/releases/v5.0.13/js/all.js", // URL
            "sha384-d84LGg2pm9KhR4mCAs3N29GQ4OYNy+K+FBHX8WhimHpPm86c839++MDABegrZ3gn", // Integrity
            "anonymous" // Cross-origin
        );
        getScript(
            "https://cdnjs.cloudflare.com/ajax/libs/ace/1.3.3/ace.js"
        );
        getScript(
            "https://cdn.jsdelivr.net/npm/flatpickr"
        );
    }
};
