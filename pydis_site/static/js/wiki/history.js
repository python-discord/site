function showPreviewModal(revision_id, action_url, change_revision_url) {
  let iframe = $("#previewWindow");

  iframe.attr("src", action_url + "?r=" + revision_id);

  console.log(revision_id);
  console.log(action_url + "?r=" + revision_id);
  console.log(change_revision_url);

  $('#previewModal .switch-to-revision').attr('href', change_revision_url);
  open_modal('previewModal');
}
