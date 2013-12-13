makePostRequest = function(data, url, onsuccess) {
	$.ajax({
		url: document.API_URL + url,
		type: 'POST',
		dataType: 'json',
		contentType: 'json',
		data: JSON.stringify(data),
		crossDomain: true,
		success: onsuccess,
		error: function(ret) {
			if (ret['status'] == 401)
				window.location.replace('/static/login.html');
		}
	});
};

makeGetRequest = function(url, onsuccess) {
	$.ajax({
		url: document.API_URL + url,
		type: 'GET',
		contentType: 'json',
		crossDomain: true,
		success: onsuccess,
		error: function(ret) {
			if (ret['status'] == 401)
				window.location.replace('/static/login.html');
		}
	});

};

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
		makePostRequest(dic, url, onsuccess);
	});
};

showAddTabForm = function(){
	makeBasicForm('Add Tab',
								[{name: 'name', placeholder: 'Aha'},
									{name: 'priority', placeholder: '10'}],
									'/add_tab',
									function(ret){
										if(ret['success'] == 1){
											$('#form-modal').modal('hide');
											setTimeout(refreshTab, 500);
										}
										if(ret['error'] !== undefined)
											alert(ret['error']);
									});
	$('#form-modal').modal('show');
};

showDeleteTabForm = function(){
	var $tab = getNowTab();
	var tabname = $tab.text();
	makeBasicForm('Delete tab "'+tabname+'" ?',
								[{name: 'name', type: 'hidden', value: tabname}],
								'/del_tab',
								function(ret){
									$('#form-modal').modal('hide');
									setTimeout(refreshTab, 500);
								});
	$('#form-modal').modal('show');
};

showEditTabForm = function(){
	var $tab = getNowTab();
	var tabname = $tab.text();
	var tags = $tab.data('tags');
	$.getJSON(document.API_URL+'/get_all_tags', '', function(alltags){
		var tagnames = $.map(alltags['tags'], function(x){return x['name'];});
		makeBasicForm('Edit tab "' + tabname + '"',
									[{name: 'tab', type: 'hidden', value: tabname},
										{
											name: 'name',
											type: 'select',
											'data-placeholder': 'Select tags for this tab.',
											multiple: '',
											style: 'width:100%;',
										}],
										'/set_tag',
										function(ret){
											if(ret['error'] !== undefined)
												alert(ret['error']);
											else{
												doRefreshTab(ret['tabs']);
												$('#form-modal').modal('hide');
											}
										});
		var $select = $('#form-name');
		$.each(tagnames, function(i, tagname){
			var $option = $('<option>').attr('value', tagname).text(tagname);
			if(tags.indexOf(tagname) != -1) $option.attr('selected', '');
			$select.append($option);
		});
		$select.chosen({width: "100%"});
		$('#form-modal').modal('show');
	});
};
