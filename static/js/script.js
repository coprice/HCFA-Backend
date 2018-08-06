function requestSubmitClicked() {

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

function resetSubmitClicked() {

  password = document.getElementById('password');
  confirm = document.getElementById('confirm');
  messageDiv = document.getElementById('messageDiv');

  if (!isSecure(password.value)) {
    messageDiv.innerHTML = '<div class="ui red message">Password must be at least 8 characters, with a capital letter and a number</div><br>';
    return false;
  }

  if (password.value != confirm.value) {
    messageDiv.innerHTML = '<div class="ui red message">Passwords do not match.</div><br>';
    return false;
  }

  messageDiv.innerHTML = '<div class="ui active centered inline loader"></div><br><br>';

  return true;
}

function isSecure(text) {
  var regex = /\d/g;
  return regex.test(text) && text.match(/[A-Z]/) && text.length > 7;
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
