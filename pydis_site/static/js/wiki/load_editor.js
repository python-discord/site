(function() {
    window.editors = {};  // So that other scripts can get at 'em

    let elements = document.getElementsByClassName("simple-mde");

    for (let element of elements) {
        window.editors[element.id] = new SimpleMDE({
            "element": element,

            autoDownloadFontAwesome: false,  // We already have the pro one loaded

            autosave: {
                enabled: false,
                // uniqueId: element.id + "@" + window.location.href,
            },

            blockStyles: {
                bold: "**",
                code: "```",
                italic: "_",
            },

            forceSync: true,
            indentWithTabs: false,
            initialValue: element.value,
            placeholder: "**Write some _markdown_!**",
            spellChecker: false,
            tabSize: 4,

            toolbar: [
                "bold", "italic", "strikethrough", {
                    name: "heading",
                    action: SimpleMDE.toggleHeadingSmaller,
                    className: "fa fa-heading",
                    title: "Heading",
                }, "|",
                "code", "quote", "unordered-list", "ordered-list", "|",
                "link", {
                    name: "image",
                    action: SimpleMDE.drawImage,
                    className: "fa fa-image",
                    title: "Insert image",
                }, "table", "horizontal-rule", "|",
                "preview", "side-by-side", "fullscreen", "|",
                "guide"
            ],
        })
    }
})();
