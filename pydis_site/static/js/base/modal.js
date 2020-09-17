/*
 modal.js: A simple way to wire up Bulma modals.

 This library is intended to be used with Bulma's modals, as described in the
 official Bulma documentation. It's based on the JavaScript that Bulma
 themselves use for this purpose on the modals documentation page.

 Note that, just like that piece of JavaScript, this library assumes that
 you will only ever want to have one modal open at once.
 */

"use strict";

// Event handler for the "esc" key, for closing modals.

document.addEventListener("keydown", (event) => {
  const e = event || window.event;

  if (e.code === "Escape" || e.keyCode === 27) {
    closeModals();
  }
});

// An array of all the modal buttons we've already set up

const modal_buttons = [];

// Public API functions

function setupModal(target) {
  // Set up a modal's events, given a DOM element. This can be
  // used later in order to set up a modal that was added after
  // this library has been run.

  // We need to collect a bunch of elements to work with
  const modal_background = Array.from(target.getElementsByClassName("modal-background"));
  const modal_close = Array.from(target.getElementsByClassName("modal-close"));

  const modal_head = Array.from(target.getElementsByClassName("modal-card-head"));
  const modal_foot = Array.from(target.getElementsByClassName("modal-card-foot"));

  const modal_delete = [];
  const modal_button = [];

  modal_head.forEach((element) => modal_delete.concat(Array.from(element.getElementsByClassName("delete"))));
  modal_foot.forEach((element) => modal_button.concat(Array.from(element.getElementsByClassName("button"))));

  // Collect all the elements that can be used to close modals
  const modal_closers = modal_background.concat(modal_close).concat(modal_delete).concat(modal_button);

  // Assign click events for closing modals
  modal_closers.forEach((element) => {
    element.addEventListener("click", () => {
      closeModals();
    });
  });

  setupOpeningButtons();
}

function setupOpeningButtons() {
  // Wire up all the opening buttons, avoiding buttons we've already wired up.
  const modal_opening_buttons = Array.from(document.getElementsByClassName("modal-button"));

  modal_opening_buttons.forEach((element) => {
    if (!modal_buttons.includes(element)) {
      element.addEventListener("click", () => {
        openModal(element.dataset.target);
      });

      modal_buttons.push(element);
    }
  });
}

function openModal(target) {
  // Open a modal, given a string ID
  const element = document.getElementById(target);

  document.documentElement.classList.add("is-clipped");
  element.classList.add("is-active");
}

function closeModals() {
  // Close all open modals
  const modals = Array.from(document.getElementsByClassName("modal"));
  document.documentElement.classList.remove("is-clipped");

  modals.forEach((element) => {
    element.classList.remove("is-active");
  });
}

(function () {
  // Set up all the modals currently on the page
  const modals = Array.from(document.getElementsByClassName("modal"));

  modals.forEach((modal) => setupModal(modal));
  setupOpeningButtons();
}());
