document.addEventListener("DOMContentLoaded", () => {
    const headers = document.getElementsByClassName("collapsible");
    for (const header of headers) {
        header.addEventListener("click", () => {
            var content = header.nextElementSibling;
            content.classList.toggle('collapsed');
        });
    }
});
