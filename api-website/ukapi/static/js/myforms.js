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
	console.log(data)
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
			var tmp = $('#form-'+input['name']).val();
			if(tmp === null) tmp = [];
			dic[input['name']] = tmp;
		});
		if($form.data('usingget'))
			$.getJSON(url, dic, onsuccess);
		else
			makePostRequest(dic, url, onsuccess);
	});
	return $form;
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
												$('#form-modal').modal('hide');
												doRefreshTab(ret['tabs']);
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

showEditFetcherForm = function(){
	$.getJSON(document.API_URL+'/fetcher/list', '', function(ret){
		var fetchers = ret['fetcher'];
		var $form = makeBasicForm('Select fetchers',
            [{name: 'fetcher',
							type: 'select',
							'data-placeholder': 'Select fetchers',
							multiple: '',
            }], '#');
		var $select = $('#form-fetcher');
		$.each(fetchers, function(i, fetcher){
			var $option = $('<option>').attr('value', fetcher['id']).text(fetcher['name']);
			if(fetcher['enabled']) $option.attr('selected', '');
			$select.append($option);
		});
		$select.chosen({width: "100%"});
		$(document).data('old-fetchers', fetchers);
		$form.off();
		$form.on('submit', function(e){
			e.preventDefault();
			$(document).data('new-fetchers', $select.val());
			$('#form-modal').modal('hide');
			setTimeout(doEditFetcher, 500);
		});
		$('#form-modal').modal('show');
	});
};

showEditFilterForm = function(){
	$.getJSON(document.API_URL+'/filter/list', '', function(ret){
		var filters = ret['filter'];
		var $form = makeBasicForm('Select filters',
            [{name: 'filter',
							type: 'select',
							'data-placeholder': 'Select filters',
							multiple: '',
            }], '#');
		var $select = $('#form-filter');
		$.each(filters, function(i, filter){
			var $option = $('<option>').attr('value', filter['id']).text(filter['name']);
			if(filter['enabled']) $option.attr('selected', '');
			$select.append($option);
		});
		$select.chosen({width: "100%"});
		$(document).data('old-filters', filters);
		$form.off();
		$form.on('submit', function(e){
			e.preventDefault();
			$(document).data('new-filters', $select.val());
			$('#form-modal').modal('hide');
			setTimeout(doEditFilter, 500);
		});
		$('#form-modal').modal('show');
	});
};

doEditFetcher = function(){
	var to_enable = [];
	var to_disable = [];
	var new_fetchers = $(document).data('new-fetchers');
	if(new_fetchers === null) new_fetchers = [];
	$.each($(document).data('old-fetchers'), function(i, fetcher){
		if(fetcher['enabled'] && new_fetchers.indexOf(fetcher['id'])==-1 ) to_disable.push(fetcher);
		if(!fetcher['enabled'] && new_fetchers.indexOf(fetcher['id'])!=-1 ) to_enable.push(fetcher);
	});
	if(to_enable.length > 0){
		var fetcher = to_enable.pop();
		fetcher['enabled'] = true;

		var formArgs = [];
		fetcher['config'].forEach(function(conf_name) {
			var c = {name: conf_name}
			if (conf_name == 'password')
				c['type'] = 'password'
			formArgs.push(c);
		});
		formArgs.push({ name: 'fetcher_id', type: 'hidden', value: fetcher['id'] });

		makeBasicForm('Configure fetcher "'+fetcher['name']+'"', formArgs,
			'/fetcher/enable',
			function(ret){
				$('#form-modal').modal('hide');
				setTimeout(doEditFetcher, 500);
			}).data('usingget', true);
		$('#form-modal').modal('show');
		return;
	}
	$.each(to_disable, function(i, fetcher){
		$.getJSON('/fetcher/disable', {fetcher_id: fetcher['id']});
	});
	setTimeout(refreshTab, 500);
};

doEditFilter = function(){
	var to_enable = [];
	var to_disable = [];
	var new_filters = $(document).data('new-filters');
	if(new_filters === null) new_filters = [];
	$.each($(document).data('old-filters'), function(i, filter){
		if(filter['enabled'] && new_filters.indexOf(filter['id'])==-1 ) to_disable.push(filter);
		if(!filter['enabled'] && new_filters.indexOf(filter['id'])!=-1 ) to_enable.push(filter);
	});
	if(to_enable.length > 0){
		var filter = to_enable.pop();
		filter['enabled'] = true;

		var formArgs = [];
		filter['config'].forEach(function(conf_name) {
			var c = {name: conf_name}
			if (name == 'password')
				c['type'] = 'password'
			formArgs.push(c);
		});
		formArgs.push({ name: 'filter_id', type: 'hidden', value: filter['id']});

		makeBasicForm('Configure filter "' + filter['name'] + '"', formArgs ,
			'/filter/enable',
			function(ret){
				$('#form-modal').modal('hide');
				setTimeout(doEditFilter, 500);
			}).data('usingget', true);
		$('#form-modal').modal('show');
		return;
	}
	$.each(to_disable, function(i, filter){
		$.getJSON('/filter/disable', {filter_id: filter['id']});
	});
	setTimeout(refreshTab, 500);
};
