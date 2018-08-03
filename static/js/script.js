function submitClicked() {

  email = document.getElementById('email');
  password = document.getElementById('password');
  messageDiv = document.getElementById('messageDiv');

  if (email.value == "") {
    messageDiv.innerHTML = '<div class="ui red message">Please enter your email.</div><br>';
    return false;
  }

  if (password.value == "") {
    messageDiv.innerHTML = '<div class="ui red message">Please enter your password.</div><br>';
    return false;
  }

  messageDiv.innerHTML = '<div class="ui active centered inline loader"></div><br><br>';

  return true;
}

$(document).ready(function() {

  $('.ui.form').form({});

  /* Text animations */
  $('h1').hide();
  $('label').hide();
  $('input').hide();

  $('h1').transition('fade up', '500ms');
  $('label').delay(500).transition('fade up', '500ms');
  $('input').delay(500).transition('fade up', '500ms');

});
