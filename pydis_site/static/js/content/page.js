document.addEventListener("DOMContentLoaded", () => {
    const headers = document.getElementsByClassName("collapsible");
    for (const header of headers) {
        header.addEventListener("click", () => {
            var content = header.nextElementSibling;
            if (content.style.maxHeight){
              content.style.maxHeight = null;
            } else {
              content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }
});