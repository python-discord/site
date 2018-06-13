"use strict";

window.onload = function () {
    const app = document.getElementById("error");

    const typewriter = new Typewriter(app, {
        "loop": false,
        "deleteSpeed": 40,
        "typingSpeed": "natural",
        "devMode": false
    });

    function closeWindow() {
        const app = document.getElementById("win");
        const current_class = app.getAttribute("class");
        app.setAttribute("class", `${current_class } uk-animation-scale-up uk-animation-reverse`);
        typewriter.stop();
    }

    document.getElementById("terminal-close").onclick = closeWindow;

    typewriter.appendText("Python 3.6.4 (default, Jan  5 2018, 02:35:40)\n")
        .appendText("[GCC 7.2.1 20171224] on darwin\n")
        .appendText("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.\n")
        .appendText(">>> ")
        .pauseFor(1000)
        .typeString("impor requests")
        .deleteChars(9)
        .typeString("t requests\n")
        .appendText(">>> ")
        .pauseFor(750)
        .changeSettings({"typingSpeed": "natural"})
        .typeString(`response = requests.${ window._RequestMethod }('https://pythim`)
        .deleteChars(2)
        .typeString("ondiscord.con/")
        .deleteChars(2)
        .typeString(`m${ window._Path }')\n`)
        .pauseFor(1000)
        .appendText(`&lt;Response [${ window._Code }]&gt;\n>>> `)
        .typeString("# hmmmm")
        .pauseFor(1000)
        .deleteChars(7)
        .pauseFor(1000)
        .typeString("response.text\n")
        .appendText(`${ window._ErrorMsg }\n>>> `)
        .start();
};
