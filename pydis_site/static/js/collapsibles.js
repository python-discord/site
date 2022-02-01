document.addEventListener("DOMContentLoaded", () => {
    // Set maxHeight to scroll height on all matching collapsibles
    const contentContainers = document.getElementsByClassName("collapsible-content");
    for (const container of contentContainers) {
        container.style.maxHeight = container.scrollHeight + "px";
    }

    const headers = document.getElementsByClassName("collapsible");
    for (const header of headers) {
        header.addEventListener("click", () => {
            var content = header.nextElementSibling;
            content.classList.toggle('collapsed');
        });
    }
});
