//<![CDATA[
(function($) {
  $(document).ready(function (){
    $("#id_title").keyup(function () {
      var e = $("#id_slug")[0];
      if(!e._changed) {
        slug = URLify(this.value, 50);
        e.value = slug;
      }
      });
  });
})(jQuery);
//]]>
