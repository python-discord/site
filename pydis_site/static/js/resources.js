"use strict";
const initialParams = new URLSearchParams(window.location.search);
const checkboxOptions = ['topic', 'type', 'payment', 'complexity'];

const createQuerySelect = (opt) => {
    return "input[name=" + opt + "]"
}

checkboxOptions.forEach((option) => {
    document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
        if (initialParams.get(option).includes(checkbox.value)) {
            checkbox.checked = true
        }
    });
});

function buildQueryParams() {
    let params = new URLSearchParams(window.location.search);
    checkboxOptions.forEach((option) => {
        let tempOut = ""
        document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
            if (checkbox.checked) {
                tempOut += checkbox.value + ",";
            }
        });
        params.set(option, tempOut);
    });

    window.location.search = params;
}

function clearQueryParams() {
    checkboxOptions.forEach((option) => {
        document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
            checkbox.checked = false;
        });
    });
}

function selectAllQueryParams(column) {
    checkboxOptions.forEach((option) => {
        document.querySelectorAll(createQuerySelect(option)).forEach((checkbox) => {
            if (checkbox.className == column) {
                checkbox.checked = true;
            }
        });
    });
}
