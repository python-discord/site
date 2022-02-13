"use strict";

// Filters that are currently selected
var activeFilters = {
    topics: [],
    type: [],
    "payment-tiers": [],
    difficulty: []
};

// Options for fuzzysort
const fuzzysortOptions = {
  allowTypo: true,    // Allow our users to make typos
  threshold: -10000,  // The threshold for the fuzziness. Adjust for precision.
};

/* Add a filter, and update the UI */
function addFilter(filterName, filterItem) {
    var filterIndex = activeFilters[filterName].indexOf(filterItem);
    if (filterIndex === -1) {
        activeFilters[filterName].push(filterItem);
    }
    updateUI();
}

/* Remove all filters, and update the UI */
function removeAllFilters() {
    activeFilters = {
        topics: [],
        type: [],
        "payment-tiers": [],
        difficulty: []
    };
    updateUI();
}

/* Remove a filter, and update the UI */
function removeFilter(filterName, filterItem) {
    var filterIndex = activeFilters[filterName].indexOf(filterItem);
    if (filterIndex !== -1) {
        activeFilters[filterName].splice(filterIndex, 1);
    }
    updateUI();
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

    // Add the search query to the search bar.
    if (searchParams.has("search")) {
        let searchQuery = searchParams.get("search");
        $("#resource-search input").val(searchQuery);
    }

    // Work through the parameters and add them to the filter object
    $.each(Object.keys(activeFilters), function(_, filterType) {
        let paramFilterContent = searchParams.get(filterType);

        if (paramFilterContent !== null) {
            // We use split here because we always want an array, not a string.
            let paramFilterArray = paramFilterContent.split(",");

            // Update the corresponding filter UI, so it reflects the internal state.
            let filterAdded = false;
            $(paramFilterArray).each(function(_, filter) {
                // Catch special cases.
                if (String(filter) === "rickroll" && filterType === "type") {
                    window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
                } else if (String(filter) === "sneakers" && filterType === "topics") {
                    window.location.href = "https://www.youtube.com/watch?v=NNZscmNE9QI";

                // If the filter is valid, mirror it to the UI.
                } else if (validFilters.hasOwnProperty(filterType) && validFilters[filterType].includes(String(filter))) {
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

            // If we've added a filter, hide stuff
            if (filterAdded) {
                $(".no-tags-selected.tag").hide();
                $(".close-filters-button").show();
            }
        }
    });
}

/* Update the URL with new parameters */
function updateURL() {
    let searchQuery = $("#resource-search input").val();

    // If there's no active filtering parameters, we can return early.
    if (noFilters() && searchQuery.length === 0) {
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

    // Add the search query, if necessary.
    if (searchQuery.length > 0) {
        searchParams.set("search", searchQuery);
    }

    // Now update the URL
    window.history.replaceState(null, document.title, `?${searchParams.toString()}`);
}

/* Apply search terms */
function filterBySearch(resourceItems) {
    let searchQuery = $("#resource-search input").val();

    /* Show and update the tag if there's a search query */
    if (searchQuery) {
        let tag = $(".tag.search-query");
        let tagText = $(".tag.search-query span");
        tagText.text(`Search: ${searchQuery}`);
        tag.show();
    }

    resourceItems.filter(function() {
        // Run a fuzzy search over the item. Does the search query match?
        let name = $(this).attr("name");
        let result = fuzzysort.single(searchQuery, name, fuzzysortOptions);
        return Boolean(result) && result.score > fuzzysortOptions.threshold;
    }).show();
}

/* Update the resources to match 'active_filters' */
function updateUI() {
    let resources = $('.resource-box');
    let filterTags = $('.filter-box-tag');
    let resourceTags = $('.resource-tag');
    let noTagsSelected = $(".no-tags-selected.tag");
    let closeFiltersButton = $(".close-filters-button");
    let searchQuery = $("#resource-search input").val();
    let searchTag = $(".tag.search-query");

    // Update the URL to match the new filters.
    updateURL();

    // If there's nothing in the filters, we can return early.
    if (noFilters()) {
        // If we have a searchQuery, we need to run all resources through a search.
        if (searchQuery.length > 0) {
            resources.hide();
            noTagsSelected.hide();
            filterBySearch(resources);
        } else {
            resources.show();
            noTagsSelected.show();
            $(".tag.search-query").hide();
        }

        filterTags.hide();
        closeFiltersButton.hide();
        resourceTags.removeClass("active");
        $(`.filter-checkbox:checked`).prop("checked", false);
        $(".no-resources-found").hide();

        return;
    } else {
        // Hide everything
        $('.filter-box-tag').hide();
        $('.resource-tag').removeClass("active");
        noTagsSelected.show();
        closeFiltersButton.hide();

        // Now conditionally show the stuff we want
        $.each(activeFilters, function(filterType, filters) {
            $.each(filters, function(index, filter) {
                // Show a corresponding filter box tag
                $(`.filter-box-tag[data-filter-name=${filterType}][data-filter-item=${filter}]`).show();

                // Make corresponding resource tags active
                $(`.resource-tag[data-filter-name=${filterType}][data-filter-item=${filter}]`).addClass("active");

                // Hide the "No filters selected" tag.
                noTagsSelected.hide();

                // Show the close filters button
                closeFiltersButton.show();
            });
        });
    }

    // Otherwise, hide everything and then filter the resources to decide what to show.
    let hasMatches = false;
    resources.hide();
    let filteredResources = resources.filter(function() {
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
    });

    // Run the items we've found through the search filter, if necessary.
    if (searchQuery.length > 0) {
        filterBySearch(filteredResources);
    } else {
        filteredResources.show();
        searchTag.hide();
    }

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

    // If this is a mobile device, collapse all the categories to win back some screen real estate.
    if (screen.width < 480) {
        let categoryHeaders = $(".filter-category-header .collapsible-content");
        let icons = $('.filter-category-header button .card-header-icon i');
        categoryHeaders.addClass("no-transition collapsed");
        icons.removeClass(["far", "fa-window-minimize"]);
        icons.addClass(["fas", "fa-angle-down"]);

        // Wait 10ms before removing this class, or else the transition will animate due to a race condition.
        setTimeout(() => { categoryHeaders.removeClass("no-transition"); }, 10);
    }

    // When you type into the search bar, trigger an UI update.
    $("#resource-search input").on("input", function() {
        updateUI();
    });

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

    // When you click the little gray x, remove all filters.
    $(".close-filters-button").on("click", function() {
        removeAllFilters();
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
