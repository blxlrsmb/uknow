
makeBasicForm = function(title, data, url, onsuccess){
    $('#form-modal h3').text(title);
    var $form = $('<form>').addClass('form-horizontal').attr('action', '#');
    $('#form-modal .modal-body').html($form);
    $.each(data, function(i, input){
        var name = 'form-' + input['name'];
        if(input['type'] === undefined) input['type'] = 'text';
        if(input['placeholder'] === undefined) input['placeholder'] = input['name'];
        $control_group = $('<div>').addClass('control-group');
        var $label = $('<label>').addClass('control-label').attr('for', name);
        $label.text(input['name'].charAt(0).toUpperCase()+input['name'].slice(1));
        if(input['type'] != 'hidden') $control_group.append($label);
        var $input = $('<input>');
        if(input['type'] == 'select') $input = $('<select>');
        $.each(input, function(n,m){
            $input.attr(n,m);
        });
        $input.attr('id', name);
        $control_group.append($('<div>').addClass('controls').append($input));
        $form.append($control_group);
    });
    $form.append($('<div class="control-group"><div class="controls" id="form-btns">'+
            '<button type="submit" class="btn">Go!</button></div></div>'));
    $form.on('submit', function(e){
        e.preventDefault();
        var dic = {};
        $.each(data, function(i, input){
            dic[input['name']] = $('#form-'+input['name']).val();
        });
        $.ajax({
            url: document.API_URL+url,
            type: 'POST',
            dataType: 'json',
            contentType: 'json',
            data: JSON.stringify(dic),
            crossDomain: true,
            success: onsuccess
        });
    });
};

showRegisterForm = function(){
    makeBasicForm('Register',
                  [{name: 'username', placeholder: 'test@example.com'},
                   {name: 'password', type: 'password', placeholder: 'xxx'}],
                  '/register',
                  function(ret){
                        if(ret['success'] == 1){
                          $('#form-modal').modal('hide');
                          alert('Register ok.');
                          setTimeout(showLoginForm, 500);
                        }
                        if(ret['error'] !== undefined)
                          alert(ret['error']);
                  });
    $('#form-modal').modal('show');
};

showLoginForm = function(){
    makeBasicForm('Login',
                  [{name: 'username', placeholder: 'test@example.com'},
                   {name: 'password', type: 'password', placeholder: 'xxx'}],
                  '/login',
                  function(ret){
                    if(ret['success'] == 1){
                      $('#form-modal').modal('hide');
                      refreshTab();
                    }
                    if(ret['error'] !== undefined)
                      alert(ret['error']);
                  });
    $('#form-btns').append($('<button>').addClass('btn btn-info').text('Register').click(function(e){
        e.preventDefault();
        $('#form-modal').modal('hide');
        setTimeout(showRegisterForm, 500);
    }));
    $('#form-modal').modal('show');
};

showAddTabForm = function(){
    makeBasicForm('Add Tab',
                  [{name: 'name', placeholder: 'Aha'},
                   {name: 'priority', placeholder: '10'}],
                  '/add_tab',
                  function(ret){
                        if(ret['success'] == 1){
                          $('#form-modal').modal('hide');
                          refreshTab();
                        }
                        if(ret['error'] !== undefined)
                          alert(ret['error']);
                  });
    $('#form-modal').modal('show');
};

showDeleteTabForm = function(tabname){
    makeBasicForm('Delete tab "'+tabname+'" ?',
                  [{name: 'name', type: 'hidden', value: tabname}],
                  '/del_tab',
                  refreshTab);
    $('#form-modal').modal('show');
};

showEditTabForm = function(tabname){
    $.getJSON(document.API_URL+'/get_all_tags', '', function(alltags){
      var tagnames = $.map(alltags['tags'], function(x){return x['name'];});
      makeBasicForm('Edit tab "' + tabname + '"?',
                    [{name: 'name', type: 'hidden', value: tabname},
                     {
                        name: 'tags',
                        type: 'select',
                        'data-placeholder': 'No tag selected',
                        multiple: '',
                        style: 'width:100%;',
                      }],
                    '/set_tags');
      var $select = $('#form-tags');
      $.each(tagnames, function(i, tagname){
        var $option = $('<option>').attr('value', tagname).text(tagname);
        $select.append($select);
      });
      $select.chosen({width: "100%"});
      $('#form-modal').modal('show');
    });
};