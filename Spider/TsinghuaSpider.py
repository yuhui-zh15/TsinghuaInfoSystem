# coding=utf-8
import urllib2
import re
import Queue
import jieba
import time
import os

os.chdir(os.getcwd()+'/list/')


class TsinghuaSpider:
	m_dict = dict()
	m_file2title = dict()
	m_file2time = dict()
	m_file2url = dict()
	m_visited = set()
	m_exception = set()
	m_queue = Queue.Queue()
	m_rooturl = 'http://news.tsinghua.edu.cn'
	m_firsturl = '/publish/thunews/index.html'
	m_cnt = int()

	def __init__(self):
		self.m_queue.put(self.m_firsturl)
		self.m_cnt = 0

	def __delete__(self):
		self.write_dict()
		self.write_other()

	def write_dict(self):
		file = open('dict.json', 'w')
		file.write(str(self.m_dict))
		file.close()

	def write_other(self):
		file = open('file2title.json', 'w')
		file.write(str(self.m_file2title))
		file.close()
		file = open('file2time.json', 'w')
		file.write(str(self.m_file2time))
		file.close()
		file = open('file2url.json', 'w')
		file.write(str(self.m_file2url))
		file.close()

	def write_file(self, filename, data, title):
		file = open(filename, 'w')
		file.write('<meta charset = \'utf-8\'>\n')
		#print title
		file.write(title)
		file.write(data)
		file.close()

	def split_word(self, filename, data):
		seg_list = jieba.cut_for_search(data)
		for seg in seg_list:
			self.m_dict.setdefault(seg, set()).add(filename)

	def get_page(self, url):
		webpage = urllib2.urlopen(url)
		data = webpage.read()
		return data

	def get_href(self, data):
		pattern = re.compile(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')")
		items = re.findall(pattern, data)
		return items

	def get_article(self, data):
		pattern = re.compile(r'<article.*?/article>', re.S)
		items = re.search(pattern, data)
		#print items.group(0)
		if items:
			return items.group(0)

	def get_title(self, data):
		pattern = re.compile(r'<title.*?/title>', re.S)
		items = re.search(pattern, data)
		if items:
			return items.group(0)

	def get_time(self, data):
		pattern = re.compile(r'<.*?articletime.*?>.*?<.*?>.*?<.*?>(.*?)<.*?>')
		items = re.search(pattern, data)
		if items:
			return items.group(1)

	def get_lastname(self, filename):
		return filename.split('/')[-1]

	def run(self):
		# BFS
		while self.m_queue.empty() is False:
			first = self.m_queue.get()
			if (first[0:17] != '/publish/thunews/'):
				continue
			if first not in self.m_visited:
				self.m_visited.add(first)
				url = self.m_rooturl + first
				try:
					data = self.get_page(url)
					hrefs = self.get_href(data)
					
					for item in hrefs:
						self.m_queue.put(item)

					article = self.get_article(data)
					if article is not None:
					
						self.m_cnt += 1
						filename = self.get_lastname(first)
						print self.m_cnt, ': ', filename
						
						self.m_file2title[filename] = self.get_title(data)
						self.m_file2time[filename] = self.get_time(data)
						self.m_file2url[filename] = url
						self.write_file(filename, article, self.get_title(data))
						self.split_word(filename, article)
						
						#导出词典
						if (self.m_cnt % 1000 == 0):
							self.write_dict()
							self.write_other()

				except Exception, e:
					print e

spider = TsinghuaSpider()
spider.run()
