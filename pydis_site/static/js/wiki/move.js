$('#id_destination').after($('#dest_selector').remove());
$('#id_destination').attr('type', 'hidden');
$('#id_slug').val('{{ urlpath.slug }}');
select_path('{{urlpath.parent.pk}}', '{{urlpath.parent}}');

function select_path(path, title) {
  $('#id_destination').val(path);
  if (title == "(root)") title = "";
  $('#dest_selector .dest_selector_title').html(title ? title : "&nbsp;&nbsp;/&nbsp;&nbsp;");
}
