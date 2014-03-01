$(document).ready(function() {
	var login = true;
	$("#account_create").click(function() {
		if(login) {
			$("#login_form").attr("action", "/register/");
			$(".registration").slideDown();
			login = false;
			return false;
		}
	});
	$("#login_button").click(function() {
		if(!login) {
			$("#login_form").attr("action", "/login/");
			$(".registration").slideUp();
			login = true;
			return false;
		}
	});
});