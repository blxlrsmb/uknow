#!/usr/bin/env python
# -*- coding=UTF-8 -*-

import sys
if hasattr(sys, 'setdefaultencoding'):
	sys.setdefaultencoding('UTF-8')

import threading
from urllib2 import URLError
from handle_str import filename_trans
from items import *
class mythread(threading.Thread):
	def __init__(self, option, output, if_format = False):
		super(mythread, self).__init__()
		self.existing = False
		self.option = option
		self.output = output
		self.if_format = if_format
		if if_format:
			self.fileroot = '.txt'
		else:
			self.fileroot = '.html'
	def run(self):
		try:
			self.existing = False
			self.unread_files = tuple()
			courses = login(self.option['user'], self.option['password'], self.option['if_this_only'])
			for i in courses:
				self.output.write(u'正在处理课程 '+i['name']+' ...\n')
				thiscourse = course(i)
				for itemtype in item_name_dict:
					for j in thiscourse.get_item_list(itemtype):
						if self.existing:
							self.output.write(u'\n\n\n\t\t下载取消，退出')
							self.output.finish(False)
							return
						thisitem = item(j, itemtype)
						thispath = os.path.join(self.option['path'], filename_trans(i['name']), item_name_dict[itemtype])
						if not os.path.exists(thispath):
							os.makedirs(thispath)
						if itemtype == 'download' or itemtype == 'homework':
							try:
								thisitem.download_data(thispath, size_limit = self.option['size_limit'], \
										type_only = self.option['type_only'], type_except = self.option['type_except'], out = self.output)
							except:
								self.output.write(u'\t\t发生未知错误，忽略此文件。')
						if itemtype == 'homework' or itemtype == 'notice':
							thisitempath = os.path.join(thispath, '_'.join([filename_trans(j['name']), j['course_id'], j['id']])+self.fileroot)
							if not os.path.exists(thisitempath):
								fout = open(thisitempath, 'wb')
								fout.write(thisitem.get_data(if_format = self.if_format, out = self.output))
								fout.close()
#								if thisitem.itemtype != 'homework' or thisitem.item_dict['is_submit'] == '0':
								self.unread_files += (thisitempath, )
			self.output.write(u'\n\n\n下载完成！\n')
			self.output.finish(True)
		except KeyboardInterrupt, SystemExit:
			pass
		except RuntimeError as error:
			self.output.write(error.message)
			self.output.finish(False)
		except URLError:
			self.output.write(u'网络连接错误。\n')
			self.output.finish(False)
		except:
			import traceback
			log = open('error.log', 'w')
			traceback.print_exc(file=log)
			log.close()
			self.output.write(u'发生未知错误，请重试。若问题依旧存在，请将error.log发送给作者，谢谢。\n')
			self.output.finish(False)
