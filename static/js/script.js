function submitClicked() {

  email = document.getElementById('email');
  password = document.getElementById('password');
  messageDiv = document.getElementById('messageDiv');

  if (email.value == "") {
    messageDiv.innerHTML = '<div class="ui red message">Please enter your email.</div><br>'
    return false;
  }

  if (password.value == "") {
    messageDiv.innerHTML = '<div class="ui red message">Please enter your password.</div><br>'
    return false;
  }

  messageDiv.innerHTML = '<div class="ui active centered inline loader"></div><br><br>'
  var url = new URL(document.URL);
  var uid = url.searchParams.get("uid");
  var cid = url.searchParams.get("cid");

  $.post( "/courses/request/complete", JSON.stringify({ 'email': email.value, 'password': password.value, 'uid': uid, 'cid': cid }))
  .done(function( data ) {
    if (data['error']) != null {
      alert(data['error'])
    }
    email.value = ""
    password.value = ""
    messageDiv.innerHTML = '<div class="ui green message">User Added!</div><br>'
  });

  return true;
}

$(document).ready(function() {

  /* Form validation */
  $('.ui.form').form({});

  /* Text animations */
  $("h1").hide();
  $("label").hide();
  $("input").hide();

  $("h1").transition("fade up", '500ms');
  $("label").delay(500).transition('fade up', '500ms');
  $("input").delay(500).transition('fade up', '500ms');

});
