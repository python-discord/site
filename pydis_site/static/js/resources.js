"use strict";

// Filters that are currently selected
var activeFilters = {
    topics: [],
    type: [],
    "payment-tiers": [],
    complexity: []
};

/* Update the resources to match 'active_filters' */
function update() {
    let resources = $('.resource-box');

    // If there's nothing in the filters, show everything and return.
    if (
        activeFilters.topics.length === 0 &&
        activeFilters.type.length === 0 &&
        activeFilters["payment-tiers"].length === 0 &&
        activeFilters.complexity.length === 0
    ) {
        resources.show();
        return;
    }

    // Otherwise, hide everything and then filter the resources to decide what to show.
    resources.hide();
    resources.filter(function() {
        let validation = {
            topics: false,
            type: false,
            'payment-tiers': false,
            complexity: false
        };
        let resourceBox = $(this);

        // Validate the filters
        $.each(activeFilters, function(filterType, activeFilters) {
            // If the filter list is empty, this passes validation.
            if (activeFilters.length === 0) {
                validation[filterType] = true;
                return;
            }

            // Otherwise, we need to check if one of the classes exist.
            $.each(activeFilters, function(index, filter) {
                if (resourceBox.hasClass(filter)) {
                    validation[filterType] = true;
                }
            });
        });

        // If validation passes, show the resource.
        if (Object.values(validation).every(Boolean)) {
            return true;
        } else {
            return false;
        }
    }).show();
}

// Executed when the page has finished loading.
document.addEventListener("DOMContentLoaded", function () {

    // If you collapse or uncollapse a filter group, swap the icon.
    $('button.collapsible').click(function() {
        let icon = $(this).find(".card-header-icon i");

        if ($(icon).hasClass("fa-window-minimize")) {
            $(icon).removeClass(["far", "fa-window-minimize"]);
            $(icon).addClass(["fas", "fa-angle-down"]);
        } else {
            $(icon).removeClass(["fas", "fa-angle-down"]);
            $(icon).addClass(["far", "fa-window-minimize"]);
        }
    });

    // Update the filters on page load to reflect URL parameters.

    // If you click on the div surrounding the filter checkbox, it clicks the checkbox.
    $('.filter-panel').click(function() {
        let checkbox = $(this).find(".filter-checkbox");
        checkbox.prop("checked", !checkbox.prop("checked"));
        checkbox.change();
    });

    // When checkboxes are toggled, trigger a filter update.
    $('.filter-checkbox').change(function () {
        let filterItem = this.dataset.filterItem;
        let filterName = this.dataset.filterName;
        let cssClass = filterName + "-" + filterItem;
        var filterIndex = activeFilters[filterName].indexOf(cssClass);

        if (this.checked) {
            if (filterIndex === -1) {
                activeFilters[filterName].push(cssClass);
            }
            update();
        } else {
            if (filterIndex !== -1) {
                activeFilters[filterName].splice(filterIndex, 1);
            }
            update();
        }
    });
});



// const initialParams = new URLSearchParams(window.location.search);
// const checkboxOptions = ['topic', 'type', 'payment', 'complexity'];
//
// const createQuerySelect = (opt) => {
//     return "input[name=" + opt + "]"
// }
//
// checkboxOptions.forEach((option) => {
//     document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
//         if (initialParams.get(option).includes(checkbox.value)) {
//             checkbox.checked = true
//         }
//     });
// });
//
// function buildQueryParams() {
//     let params = new URLSearchParams(window.location.search);
//     checkboxOptions.forEach((option) => {
//         let tempOut = ""
//         document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
//             if (checkbox.checked) {
//                 tempOut += checkbox.value + ",";
//             }
//         });
//         params.set(option, tempOut);
//     });
//
//     window.location.search = params;
// }
//
// function clearQueryParams() {
//     checkboxOptions.forEach((option) => {
//         document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
//             checkbox.checked = false;
//         });
//     });
// }
//
// function selectAllQueryParams(column) {
//     checkboxOptions.forEach((option) => {
//         document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
//             if (checkbox.className == column) {
//                 checkbox.checked = true;
//             }
//         });
//     });
// }
