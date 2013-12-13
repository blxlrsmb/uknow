# -*- coding=UTF-8 -*-

from handle_str import *
from HTMLParser import HTMLParser
class itemlist_parser(HTMLParser):
	def __init__(self, feed_data, itemtype):
		HTMLParser.__init__(self)
		self.is_item = False
		self.is_itemtable = False
		self.items = tuple()
		self.itemtype = itemtype
#		WTF 'HTMLParseError: malformed start tag'
		if itemtype == 'homework':
			feed_data = delete_input(feed_data)
		self.feed(feed_data)
	def handle_starttag(self, tag, attrs):
		try:
			if tag == 'table' and attrs[0] == ('id', 'table_box'):
				self.is_itemtable = True
			if self.is_itemtable and self.check_is_item(tag, attrs):
				self.is_item = True
				for i in attrs:
					if 'href' in i:
						href_str = i[1]
				self.item_dict = urldecode(href_str)
				if self.itemtype == 'homework':
					self.item_dict['time'] = ''
		except IndexError:
			pass
	def handle_data(self, data):
		if self.is_item:
			self.item_dict['name'] = delete_space(data)
			if len(self.item_dict['name']) == 0:
				return
			self.is_item = False
			self.items = self.items + (self.item_dict, )
		if self.itemtype == 'homework':
			if is_datetime(data):
				self.items[-1]['time'] += data
			if delete_space(data).decode('UTF-8') == u'已经提交':
				self.items[-1]['is_submit'] = '1'
			if delete_space(data).decode('UTF-8') == u'尚未提交':
				self.items[-1]['is_submit'] = '0'

	def check_is_item(self, tag, attrs):
		if self.itemtype == 'notice' or self.itemtype == 'homework':
			if tag == 'a' and attrs[0][0] == 'href':
				return True
			return False
		if self.itemtype == 'download':
			if tag == 'a' and attrs[0] == ('target', '_top') and attrs[1][0] == 'href':
				return True
			return False
		raise RuntimeError('Unknown item type')

class courselist_parser(HTMLParser):
	def __init__(self, feed_data):
		HTMLParser.__init__(self)
		self.courses = tuple()
		self.is_course = False
		self.is_coursename = False
		self.is_homework = False
		self.feed(feed_data)

	def handle_starttag(self, tag, attrs):
		try:
			if tag == 'tr' and attrs[0][0] == 'class':
				self.is_course = True
			if self.is_course and tag == 'a' and attrs[0][0] == 'href':
				self.course_dict = urldecode(attrs[0][1])
				self.is_coursename = True
			if self.is_course and tag == 'span' and attrs[0] == ('class', 'red_text'):
				self.is_homework = True
		except IndexError:
			pass

	def handle_data(self, data):
		if self.is_coursename:
			self.course_dict['name'] = delete_space(data).rpartition('(')[0].rpartition('(')[0]
			self.is_coursename = False
		if self.is_homework:
			self.course_dict['homework'] = data
			self.is_homework = False
			self.is_course = False
			self.courses = self.courses + (self.course_dict, )
