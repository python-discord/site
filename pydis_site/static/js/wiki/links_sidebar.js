$(document).ready(function() {
  function search(query) {
    query = encodeURIComponent(query);
    return fetch(window.links_fetch_url + `?query=${query}`).then(function(response) {
      return response.json();
    }).then(function(data){
      return data.map(function(element) {
        return {label: element, value: element};
      })
    });
  }

  function selected(state) {
    let value = state.value;
    wikiInsertLink(value);
    document.getElementById("page_title_input").value = "";
  }

  bulmahead("page_title_input", "page_title_menu", search, selected, 10);
});

function wikiInsertLink(value) {
  let editor = window.editors["id_content"];

  editor.insert_text(value);
}

function setFetchURL(url) {
  window.links_fetch_url = url;
}
