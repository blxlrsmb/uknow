redirectLoginPage = function(){window.location.replace('/static/login.html');};

checkLogin = function() {
  $('#loading').modal('show');
  $.getJSON('/test_login', '', function(){
    $('#loading').modal('hide');
    setTimeout(refreshTab, 300);
  }).fail(redirectLoginPage);
};

doLogout = function(){
  $('#loading').modal('show');
  $.getJSON(document.API_URL + '/logout', '', function(ret){
    $('#loading').modal('hide');
    $('#login').modal('show');
    showBlackface();
  });
};

showBlackface = function(){
  $('body').html('');
  $('body').attr('style','background-color: #000000;');
  var $div = $('<div>').attr('style', 'margin: 150px auto');
  $div.append($('<img>').attr('src', 'img/logo.svg').attr('style','padding-left:40%'));
  $('body').append($div);
  var sound = new Audio('img/haha.mp3');
  sound.play();
};
