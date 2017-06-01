$("#menu-icon").on("click", function() {
	$("nav").slideToggle("fast")
});

$(window).on("resize", function() {
  if ($("#menu-icon").is(":hidden")) {
    $("nav").show();
  } else {
		$("nav").hide();
	}
});
