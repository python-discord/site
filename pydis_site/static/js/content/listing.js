/**
 * Trim a tag listing to only show a few lines of content.
 */
function trimTag() {
    const containers = document.getElementsByClassName("tag-container");
    for (const container of containers) {
        if (container.textContent.startsWith("Contains the following tags:")) {
            // Tag group, no need to trim
            continue;
        }

        // Remove every element after the first two paragraphs
        while (container.children.length > 2) {
            container.removeChild(container.lastChild);
        }

        // Trim down the elements if they are too long
        const containerLength = container.textContent.length;
        if (containerLength > 300) {
            if (containerLength - container.firstChild.textContent.length > 300) {
                // The first element alone takes up more than 300 characters
                container.removeChild(container.lastChild);
            }

            let last = container.lastChild.lastChild;
            while (container.textContent.length > 300 && container.lastChild.childNodes.length > 0) {
                last = container.lastChild.lastChild;
                last.remove();
            }

            if (container.textContent.length > 300 && (last instanceof HTMLElement && last.tagName !== "CODE")) {
                // Add back the final element (up to a period if possible)
                const stop = last.textContent.indexOf(".");
                last.textContent = last.textContent.slice(0, stop > 0 ? stop + 1: null);
                container.lastChild.appendChild(last);
            }
        }
    }
}

trimTag();
