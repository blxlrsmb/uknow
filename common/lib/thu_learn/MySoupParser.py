#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at May 29 15:48 by BlahGeek@Gmail.com

import sys
if hasattr(sys, 'setdefaultencoding'):
	sys.setdefaultencoding('UTF-8')

import re
from handle_str import *
from BeautifulSoup import BeautifulSoup
class courselist_parser_soup(BeautifulSoup):
	def __init__(self, feed_data):
		BeautifulSoup.__init__(self, feed_data)
		self.courses = tuple()
		_courselist = self.findAll(name="tr", attrs={"class":re.compile("info_tr.*")})
		for i in _courselist:
			tmp = i.find(name='a')
			course_dict = urldecode(tmp.get("href"))
			course_dict['name'] = tmp.text.rpartition('(')[0].rpartition('(')[0].strip()
			#course_dict['homework'] = i.find(name="span", attrs={"class":"red_text"}).text.strip()
			self.courses += (course_dict, )

class termlist_parser_soup(BeautifulSoup):
	def __init__(self, feed_data):
		BeautifulSoup.__init__(self, feed_data)
		self.terms = tuple()
		_termlist = self.findAll(name='td', attrs={'class':'common_c2'})
		for i in _termlist:
			tmp = i.find(name='a', attrs={'href':re.compile('^MyCourse.jsp.*')})
			if tmp == None:
				continue
			term_dict = dict()
			term_dict['name'] = tmp.text.strip()
			term_dict['url'] = tmp.get('href')
			self.terms += (term_dict, )

class itemlist_parser_soup(BeautifulSoup):
	def __init__(self, feed_data, itemtype):
		BeautifulSoup.__init__(self, feed_data)
		_itemlist = self.findAll(name="tr", attrs={"class":re.compile("tr[12]")})
		self.items = tuple()
		for i in _itemlist:
			tmp = i.find("a")
			item_dict = urldecode(tmp.get("href"))
			item_dict['name'] = tmp.text.strip()
			if itemtype == 'homework':
				item_dict['is_submit'] = i.findAll(name="td")[3].text.strip()
				item_dict['time'] = i.findAll(name="td")[2].text.strip()
			self.items += (item_dict, )
