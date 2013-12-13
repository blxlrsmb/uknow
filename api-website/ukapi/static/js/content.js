
appendNewSummary = function(source, tags, title){
  var $pubname = $('<div>').addClass('span6 pub-name').text(source);
  var $pubdate = $('<div>').addClass('span6 pub-date');
  $.map(tags, function(t, i){
    $pubdate.append(' ').append($('<span>').addClass('label').text(t));
  });
  var $article = $('<article>').addClass('well summary');
  $article.append($('<div>').addClass('row-fluid').append($pubname).append($pubdate));
  $article.append($('<h3>').addClass('pub-title').text(title));
  $('#summaries').append($article);
  return $article;
};

setArticle = function(source, title, author, content){
  $('#article-source').text(source);
  $('#article-title').text(title);
  $('#article-author').text(author);
  $('#article-content').html(content);
};

refreshTab = function(){
  $('#loading').modal('show');
  $.getJSON(document.API_URL+'/get_all_tabs', '', function(ret){
    if(ret['tabs'] === undefined){
      alert('Error refreshing tabs');
    } else {
      $tabs = $('#tabs').html('');
      ret['tabs'].sort(function(a,b){
        return (parseInt(a['priority'], 10) > parseInt(b['priority'], 10));
      });
      $.each(ret['tabs'], function(i,t){
        $tabs.append($('<li>').addClass('divider-vertical'));
        var $a = $('<a>').text(t['name']).attr('href','#');
        $a.click(function(e){
          e.preventDefault();
          focusTab($(this).parent());
        });
        $tabs.append($('<li>').addClass('itemCount').append($a));
      });
      $tabs.append($('<li>').addClass('divider-vertical'));
      focusTab(0);
      $('#loading').modal('hide');
    }
  });
};

getNowTab = function(){
  return $('.itemCount.active').text();
};

focusTab = function(n){
  $.each($('.itemCount'), function(i, tab){
    var $tab = $(tab);
    if($tab.is(n) || (typeof(n)=="number"&&i==n) || (typeof(n)=="string"&&n==$tab.text()))
      $tab.addClass('active');
    else
      $tab.removeClass('active');
  });
};
