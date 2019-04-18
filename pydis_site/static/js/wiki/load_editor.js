(function() {
    window.editors = {};  // So that other scripts can get at 'em

    const headingAction = {
        name: "heading",
        action: SimpleMDE.toggleHeadingSmaller,
        className: "fa fa-heading",
        title: "Heading",
    };
    const imageAction = {
        name: "image",
        action: SimpleMDE.drawImage,
        className: "fa fa-image",
        title: "Insert image",
    };

    const imageAlign = "align:{ALIGN} ";
    const imageSize = "size:{SIZE}";

    let elements = document.getElementsByClassName("simple-mde");

    function add_insert_image_wiki(editor) {
        editor.insert_image_wiki = function(id, align, size, caption) {
            let contents = "",
                doc = editor.codemirror.getDoc(),
                cursor = doc.getCursor();

            if (typeof align !== "undefined" && align.length) {
                contents = contents + imageAlign.replace("{ALIGN}", align);
            }

            if (typeof size !== "undefined" && size.length) {
                contents = contents + imageSize.replace("{SIZE}", size);
            }

            contents = `\n[image:${id} ${contents}]`;

            if (typeof caption !== "undefined" && caption.length) {
                contents = contents + "\n" + `    ${caption}`
            }

            doc.replaceRange(contents, cursor);
        }
    }

    function add_insert_text(editor) {
        editor.insert_text = function(text) {
            let doc = editor.codemirror.getDoc(),
                cursor = doc.getCursor();

            doc.replaceRange(text, cursor);
        }
    }

    for (let element of elements) {
        let editor = new SimpleMDE({
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
            lineWrapping: true,
            placeholder: "**Write some _markdown_!**",
            spellChecker: false,
            tabSize: 4,

            toolbar: [
                "bold", "italic", "strikethrough", headingAction, "|",
                "code", "quote", "unordered-list", "ordered-list", "|",
                "link", imageAction, "table", "horizontal-rule", "|",
                "preview", "side-by-side", "fullscreen", "|",
                "guide"
            ],

            status: false,
        });

        add_insert_image_wiki(editor);
        add_insert_text(editor);

        window.editors[element.id] = editor;
    }
})();
