import urllib
def urldecode(url):
	ans = dict()
	url = url.partition(r'?')[2]
	item_list = url.split(r'&')
	for i in item_list:
		ans[urllib.unquote(i.partition(r'=')[0])] = urllib.unquote(i.partition(r'=')[2])
	return ans

def delete_space(data):
	white_str = ' \r\t\n'
	return data.lstrip(white_str).rstrip(white_str)
def delete_input(data):
	tmp = data.split(r"<input ")
	ans = ''
	for i in tmp:
		ans += i.partition(r'/>')[2]
	return ans

def filename_trans(data):
	ex_char = ('\\', r'/', r'*', r'"', r'<', r'>', r'|', r':', r'?')
	for i in ex_char:
		data = data.replace(i, '_')
	return data

def is_datetime(data):
	if len(data) == 10 and data[4] == '-' and data[7] == '-':
		return True
	return False

def urlencode(_dic):
	dic = dict(_dic)
	for i in dic:
		dic[i] = dic[i].encode('UTF-8')
	return urllib.urlencode(dic)
