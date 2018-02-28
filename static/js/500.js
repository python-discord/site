        var app = document.getElementById('error');

        var typewriter = new Typewriter(app, {
            loop: false,
            deleteSpeed: 40,
            typingSpeed: "natural",
            devMode: false
        });



        typewriter.appendText('Python 3.6.4 (default, Jan  5 2018, 02:35:40)\n')
            .appendText('[GCC 7.2.1 20171224] on linux\n')
            .appendText('Type "help", "copyright", "credits" or "license" for more information.\n')
            .appendText('>>> ')
            .pauseFor(1000)
            .typeString("impor requests")
            .deleteChars(9)
            .typeString("t requests\n")
            .appendText(">>> ")
            .pauseFor(750)
            .changeSettings({typingSpeed: "natural"})
            .typeString("response = requests.{{ request.method.lower() }}('https://pythim")
            .deleteChars(2)
            .typeString("ondiscord.con/")
            .deleteChars(2)
            .typeString("m{{request.path}}')\n")
            .pauseFor(1000)
            .appendText("&lt;Response [{{ code }}]&gt;\n>>> ")
            .typeString("# hmmmm")
            .pauseFor(1000)
            .deleteChars(7)
            .pauseFor(1000)
            .typeString("response.text\n")
            .appendText("'An error occured while processing this request, please try again later, if this error persists please open an issue on our GitHub (https://github.com/discord-python/site/issues)'\n>>> ")
            .start();
