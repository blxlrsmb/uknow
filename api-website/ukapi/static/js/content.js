
appendNewSummary = function(data){
  var $pubname = $('<div>').addClass('span6 pub-name').text(data['source']);
  var $article = $('<article>').addClass('well summary');
  $article.append($('<div>').addClass('row-fluid').append($pubname));
  $article.append($('<h3>').addClass('pub-title').text(data['title']));
  $('#summaries').append($article);
  return $article;
};

setArticle = function(data){
  var $source = $('#article-source').html('');
  $source.text(data['time']+"  ");
  $.each(data['tags'], function(i, tag){
    $source.appent($('<span class="label">').text(tag));
  });
  $('#article-title').text(data['title']);
  $('#article-content').html(data['content']);
  var link = data['url'];
  $('#article-author').html($('<a>').attr('href', link).attr('target', '_blank').text(link));
};

doRefreshTab = function(tabs){
  var $tabs = $('#tabs').html('');
  tabs.sort(function(a,b){
    return (parseInt(a['priority'], 10) > parseInt(b['priority'], 10));
  });
  $.each(tabs, function(i,t){
    $tabs.append($('<li>').addClass('divider-vertical'));
    var $a = $('<a>').text(t['name']).attr('href','#');
    $a.click(function(e){
      e.preventDefault();
      focusTab($(this).parent());
    });
    var $li = $('<li>').addClass('itemCount').append($a);
    $li.data('tags', t['tags']);
    $tabs.append($li);
  });
  $tabs.append($('<li>').addClass('divider-vertical'));
  setTimeout(focusTab, 500, 0);
};

refreshTab = function(){
  $('#loading').modal('show');
  $.getJSON(document.API_URL+'/get_all_tabs', '', function(ret){
    if(ret['tabs'] === undefined){
      alert('Error refreshing tabs');
    } else {
      doRefreshTab(ret['tabs']);
    }
  });
};

getNowTab = function(){
  return $('.itemCount.active');
};

focusTab = function(n){
  $.each($('.itemCount'), function(i, tab){
    var $tab = $(tab);
    if($tab.is(n) || (typeof(n)=="number"&&i==n) || (typeof(n)=="string"&&n==$tab.text()))
      $tab.addClass('active');
    else
      $tab.removeClass('active');
  });
  setWholePageArticle();
};

getNowArticle = function(){
  return $('.well.summary.active');
};

focusArticle = function(n, scroll){
  $.each($('.well.summary'), function(i, article){
    var $article = $(article);
    if($article.is(n) || (typeof(n)=="number"&&i==n)){
      $article.addClass('active');
      if(scroll !== undefined && scroll)
        $('#summaries').scrollTo($article);
      var data = $article.data('data');
      setArticle(data);
    }
    else
      $article.removeClass('active');
  });
};

prevArticle = function(){
  var $prev = getNowArticle().prev();
  if($prev.length === 0) return;
  focusArticle($prev, true);
};
nextArticle = function(){
  var $next = getNowArticle().next();
  if($next.length === 0) return;
  focusArticle($next, true);
};

setWholePageArticle = function(){
    $('#loading').modal('show');
    var $tab = getNowTab();
    if($tab.length === 0){
      $('#loading').modal('hide');
      return;
    }
    var tabname = $tab.text();
    $.getJSON(document.API_URL+'/get_tab_article',
              {tab: tabname},
              function(ret){
                var $summaries = $('#summaries').html('');
                if(ret['data'].length === 0){
                  setArticle({
                    time: 'Aha!',
                    title: 'No article here!',
                    url: 'http://uknow.net9.org',
                    content: 'rt',
                    tags: []
                  });
                }
                $.each(ret['data'], function(i, article){
                    var $article = appendNewSummary(article);
                    $article.data('data', article);
                    $article.click(function(e){
                      e.preventDefault();
                      focusArticle($(this));
                    });
                    $summaries.append($article);
                });
                focusArticle(0, true);
                $('#loading').modal('hide');
              });
};

refresh = function(){
  $('#loading').modal('show');
  $.getJSON('/refresh', '', function(ret){
    $('#loading').modal('hide');
  });
};