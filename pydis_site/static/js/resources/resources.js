"use strict";

// Filters that are currently selected
var activeFilters = {
    topics: [],
    type: [],
    "payment-tiers": [],
    difficulty: []
};

function addFilter(filterName, filterItem) {
    // Push the filter into the stack
    var filterIndex = activeFilters[filterName].indexOf(filterItem);
    if (filterIndex === -1) {
        activeFilters[filterName].push(filterItem);
    }
    updateUI();

    // Show a corresponding filter box tag
    $(`.filter-box-tag[data-filter-name=${filterName}][data-filter-item=${filterItem}]`).show();

    // Make corresponding resource tags active
    $(`.resource-tag[data-filter-name=${filterName}][data-filter-item=${filterItem}]`).addClass("active");

    // Hide the "No filters selected" tag.
    $(".no-tags-selected.tag").hide();
}

function removeFilter(filterName, filterItem) {
    // Remove the filter from the stack
    var filterIndex = activeFilters[filterName].indexOf(filterItem);
    if (filterIndex !== -1) {
        activeFilters[filterName].splice(filterIndex, 1);
    }
    updateUI();

    // Hide the corresponding filter box tag
    $(`.filter-box-tag[data-filter-name=${filterName}][data-filter-item=${filterItem}]`).hide();

    // Make corresponding resource tags inactive
    $(`.resource-tag[data-filter-name=${filterName}][data-filter-item=${filterItem}]`).removeClass("active");

    // Show "No filters selected" tag, if there are no filters active
    if (noFilters()) {
        $(".no-tags-selected.tag").show();
    }
}

/* Check if there are no filters */
function noFilters() {
    return (
        activeFilters.topics.length === 0 &&
        activeFilters.type.length === 0 &&
        activeFilters["payment-tiers"].length === 0 &&
        activeFilters.difficulty.length === 0
    );
}

/* Get the params out of the URL and use them. This is run when the page loads. */
function deserializeURLParams() {
    let searchParams = new window.URLSearchParams(window.location.search);

    // Work through the parameters and add them to the filter object
    $.each(Object.keys(activeFilters), function(_, filterType) {
        let paramFilterContent = searchParams.get(filterType);

        if (paramFilterContent !== null) {
            // We use split here because we always want an array, not a string.
            let paramFilterArray = paramFilterContent.split(",");

            // Update the corresponding filter UI, so it reflects the internal state.
            let filterAdded = false;
            $(paramFilterArray).each(function(_, filter) {
                // Make sure the filter is valid before we do anything.
                if (String(filter) === "rickroll" && filterType === "type") {
                    window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
                } else if (String(filter) === "sneakers" && filterType === "topics") {
                    window.location.href = "https://www.youtube.com/watch?v=NNZscmNE9QI";
                } else if (validFilters[filterType].includes(String(filter))) {
                    let checkbox = $(`.filter-checkbox[data-filter-name='${filterType}'][data-filter-item='${filter}']`);
                    let filterTag = $(`.filter-box-tag[data-filter-name='${filterType}'][data-filter-item='${filter}']`);
                    let resourceTags = $(`.resource-tag[data-filter-name='${filterType}'][data-filter-item='${filter}']`);
                    checkbox.prop("checked", true);
                    filterTag.show();
                    resourceTags.addClass("active");
                    activeFilters[filterType].push(filter);
                    filterAdded = true;
                }
            });

            // Ditch all the params from the URL, and recalculate the URL params
            updateURL();

            // If we've added a filter, hide the no filters tag.
            if (filterAdded) {
                $(".no-tags-selected.tag").hide();
            }
        }
    });
}

/* Update the URL with new parameters */
function updateURL() {
    // If there's nothing in the filters, we don't want anything in the URL.
    if (noFilters()) {
        window.history.replaceState(null, document.title, './');
        return;
    }

    // Iterate through and get rid of empty ones
    let searchParams = new URLSearchParams(activeFilters);
    $.each(activeFilters, function(filterType, filters) {
        if (filters.length === 0) {
            searchParams.delete(filterType);
        }
    });

    // Now update the URL
    window.history.replaceState(null, document.title, `?${searchParams.toString()}`);
}

/* Update the resources to match 'active_filters' */
function updateUI() {
    let resources = $('.resource-box');
    let filterTags = $('.filter-box-tag');

    // Update the URL to match the new filters.
    updateURL();

    // If there's nothing in the filters, show everything and return.
    if (noFilters()) {
        resources.show();
        filterTags.hide();
        return;
    }

    // Otherwise, hide everything and then filter the resources to decide what to show.
    let hasMatches = false;
    resources.hide();
    resources.filter(function() {
        let validation = {
            topics: false,
            type: false,
            'payment-tiers': false,
            difficulty: false
        };
        let resourceBox = $(this);

        // Validate the filters

        $.each(activeFilters, function(filterType, filters) {
            // If the filter list is empty, this passes validation.
            if (filters.length === 0) {
                validation[filterType] = true;
                return;
            }

            // Otherwise, we need to check if one of the classes exist.
            $.each(filters, function(index, filter) {
                if (resourceBox.hasClass(`${filterType}-${filter}`)) {
                    validation[filterType] = true;
                }
            });
        });

        // If validation passes, show the resource.
        if (Object.values(validation).every(Boolean)) {
            hasMatches = true;
            return true;
        } else {
            return false;
        }
    }).show();


    // If there are no matches, show the no matches message
    if (!hasMatches) {
        $(".no-resources-found").show();
    } else {
        $(".no-resources-found").hide();
    }
}

// Executed when the page has finished loading.
document.addEventListener("DOMContentLoaded", function () {
    /* Check if the user has navigated to one of the old resource pages,
       like pydis.com/resources/communities. In this case, we'll rewrite
       the URL before we do anything else. */
    let resourceTypeInput = $("#resource-type-input").val();
    if (resourceTypeInput !== "None") {
        window.history.replaceState(null, document.title, `../?type=${resourceTypeInput}`);
    }

    // Update the filters on page load to reflect URL parameters.
    $('.filter-box-tag').hide();
    deserializeURLParams();
    updateUI();

    // If you collapse or uncollapse a filter group, swap the icon.
    $('button.collapsible').on("click", function() {
        let icon = $(this).find(".card-header-icon i");

        if ($(icon).hasClass("fa-window-minimize")) {
            $(icon).removeClass(["far", "fa-window-minimize"]);
            $(icon).addClass(["fas", "fa-angle-down"]);
        } else {
            $(icon).removeClass(["fas", "fa-angle-down"]);
            $(icon).addClass(["far", "fa-window-minimize"]);
        }
    });

    // If this is a mobile device, collapse the categories to win back some screen real estate.
    if (screen.width < 480) {
        let categoryHeaders = $(".filter-category-header .collapsible-content");
        let icons = $('.filter-category-header button .card-header-icon i');
        categoryHeaders.addClass("no-transition");
        categoryHeaders.css("max-height", "");
        icons.removeClass(["far", "fa-window-minimize"]);
        icons.addClass(["fas", "fa-angle-down"]);
        categoryHeaders.removeClass("no-transition");
    }

    // If you click on the div surrounding the filter checkbox, it clicks the corresponding checkbox.
    $('.filter-panel').on("click",function(event) {
        let hitsCheckbox = Boolean(String(event.target));

        if (!hitsCheckbox) {
            let checkbox = $(this).find(".filter-checkbox");
            checkbox.prop("checked", !checkbox.prop("checked"));
            checkbox.trigger("change");
        }
    });

    // If you click on one of the tags in the filter box, it unchecks the corresponding checkbox.
    $('.filter-box-tag').on("click", function() {
        let filterItem = this.dataset.filterItem;
        let filterName = this.dataset.filterName;
        let checkbox = $(`.filter-checkbox[data-filter-name='${filterName}'][data-filter-item='${filterItem}']`);

        removeFilter(filterName, filterItem);
        checkbox.prop("checked", false);
    });

    // If you click on one of the tags in the resource cards, it clicks the corresponding checkbox.
    $('.resource-tag').on("click", function() {
        let filterItem = this.dataset.filterItem;
        let filterName = this.dataset.filterName;
        let checkbox = $(`.filter-checkbox[data-filter-name='${filterName}'][data-filter-item='${filterItem}']`);

        if (!$(this).hasClass("active")) {
            addFilter(filterName, filterItem);
            checkbox.prop("checked", true);
        } else {
            removeFilter(filterName, filterItem);
            checkbox.prop("checked", false);
        }
    });

    // When checkboxes are toggled, trigger a filter update.
    $('.filter-checkbox').on("change", function (event) {
        let filterItem = this.dataset.filterItem;
        let filterName = this.dataset.filterName;

        if (this.checked && !activeFilters[filterName].includes(filterItem)) {
            addFilter(filterName, filterItem);
        } else if (!this.checked && activeFilters[filterName].includes(filterItem)) {
            removeFilter(filterName, filterItem);
        }
    });
});
