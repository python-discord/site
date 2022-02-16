/*
A utility for creating simple collapsible cards.

To see this in action, go to /resources or /pages/guides/pydis-guides/contributing/bot/

// HOW TO USE THIS //
First, import this file and the corresponding css file into your template.

  <link rel="stylesheet" href="{% static "css/collapsibles.css" %}">
  <script defer src="{% static "js/collapsibles.js" %}"></script>

Next, you'll need some HTML that these scripts can interact with.

<div class="card">
    <button type="button" class="card-header collapsible">
        <span class="card-header-title subtitle is-6 my-2 ml-2">Your headline</span>
        <span class="card-header-icon">
            <i class="fas fa-fw fa-angle-down title is-5" aria-hidden="true"></i>
        </span>
    </button>
    <div class="collapsible-content collapsed">
        <div class="card-content">
            You can put anything you want here. Lists, more divs, flexboxes, images, whatever.
        </div>
    </div>
</div>

That's it! Collapsing stuff should now work.
 */

document.addEventListener("DOMContentLoaded", () => {
    const contentContainers = document.getElementsByClassName("collapsible-content");
    for (const container of contentContainers) {
        // Close any collapsibles that are marked as initially collapsed
        if (container.classList.contains("collapsed")) {
            container.style.maxHeight = "0px";
        // Set maxHeight to the size of the container on all other containers.
        } else {
            container.style.maxHeight = container.scrollHeight + "px";
        }
    }

    // Listen for click events, and collapse or explode
    const headers = document.getElementsByClassName("collapsible");
    for (const header of headers) {
        const content = header.nextElementSibling;
        const icon = header.querySelector(".card-header-icon i");

        // Any collapsibles that are not initially collapsed needs an icon switch.
        if (!content.classList.contains("collapsed")) {
            icon.classList.remove("fas", "fa-angle-down");
            icon.classList.add("far", "fa-window-minimize");
        }

        header.addEventListener("click", () => {
            if (content.style.maxHeight !== "0px"){
                content.style.maxHeight = "0px";
                icon.classList.remove("far", "fa-window-minimize");
                icon.classList.add("fas", "fa-angle-down");
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                icon.classList.remove("fas", "fa-angle-down");
                icon.classList.add("far", "fa-window-minimize");
            }
        });
    }
});
