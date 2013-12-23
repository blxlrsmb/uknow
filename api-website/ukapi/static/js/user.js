redirectLoginPage = function(){window.location.replace('/static/login.html');};

checkLogin = function() {
  set_loading(1);
  $.getJSON('/test_login', '', function(){
    setTimeout(refreshTab, 500);
  }).fail(redirectLoginPage);
};

doLogout = function(){
  set_loading(1);
  $.getJSON(document.API_URL + '/logout', '', function(ret){
    set_loading(0);
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
