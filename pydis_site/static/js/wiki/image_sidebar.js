$("#id_image_insert").click(function(e) {
e.preventDefault();

let image_id_element = document.getElementById("img_id"),
    align_element = document.getElementById("img_align"),
    size_element = document.getElementById("img_size"),
    caption_element = document.getElementById("img_caption"),

    editor = window.editors["id_content"];

editor.insert_image_wiki(
    image_id_element.value, align_element.value,
    size_element.value, caption_element.value
);

$("#imgModal").removeClass("is-active");  // Close modal

// Reset form
image_id_element.value = 0;
align_element.selectedIndex = 0;
size_element.selectedIndex = 0;
caption_element.value = "";
});

function insert_image(image_id) {
document.getElementById("img_id").value = image_id;
open_modal("imgModal");
}

function add_image(form) {
  $(form).submit();
}
