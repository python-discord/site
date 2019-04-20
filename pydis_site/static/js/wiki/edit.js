$(document).ready(function() {
  let article_edit_form = $("#article_edit_form");
  let click_time = 0;

  $("#article_edit_form :input").change(function() {
     article_edit_form.data("changed",true);
  });

  if (article_edit_form.find(".alert-danger").length > 0 || article_edit_form.find(".has-error").length > 0 ) {
    // Set the forms status as "changed" if there was a submission error
    article_edit_form.data("changed",true);
  }

  window.onbeforeunload = confirmOnPageExit;

  article_edit_form.on("submit", function (ev) {
      now = Date.now();
      elapsed = now-click_time;
      click_time = now;
      if (elapsed < 3000)
          ev.preventDefault();
      window.onbeforeunload = null;
      return true;
  });
  $("#id_preview").click(function () {
      open_modal("previewModal");
      return true;
  });
  $("#id_preview_save_changes").on("click", function (ev) {
      ev.preventDefault();
      $("#id_save").trigger("click");
  });
});

var confirmOnPageExit = function (e) {
  if ($("#article_edit_form").data("changed")) {
    e = e || window.event;
    var message = "You have unsaved changes!";
    // For IE6-8 and Firefox prior to version 4
    if (e) {
        e.returnValue = message;
    }
    // For Chrome, Safari, IE8+ and Opera 12+
    return message;
  } else {
    // If the form hasn't been changed, don't display the pop-up
    return;
  }
};

$(document).ready( function() {
  $('.sidebar-form').each(function () {
    $(this).submit( function() {
      this.unsaved_article_title.value = $('#id_title').val();
      this.unsaved_article_content.value = $('#id_content').val();
    });
  });
});
