# -*- coding: utf-8 -*-
import requests, re, sqlite3, time
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import quote

class common:
	def findstr(self, rule, string):
		find_str = re.compile(rule)
		return find_str.findall(string)
	def mstr(self, string):
		return string.encode('gbk', 'ignore').decode('gbk')

class weblib:
	def __init__(self):
		self.headers = {}
		self.jar = requests.cookies.RequestsCookieJar()
	def get(self, url, chardet=False):
		try:
			req = requests.get(url, headers = self.headers, cookies = self.jar, timeout=90)
			if chardet:
				req.encoding = requests.utils.get_encodings_from_content(req.text)[0]
			return req.text
		except:
			return ''
	def post(self, url, postdata, chardet=False):
		try:
			req = requests.post(url, headers = self.headers, data = postdata, timeout=90)
			if chardet:
				req.encoding = requests.utils.get_encodings_from_content(req.text)[0]
			return req.text
		except:
			return ''

class buka:
	def __init__(self, db):
		self.db = db
		self.webpc = weblib()
		self.webpc.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
		self.webm = weblib()
		self.webm.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0.0)'}
		self.startId = self.getStart()
		self.newestId = self.getNewest()
		self.dbTime = self.getDbTime()
	def getDbTime(self):
		for line in sqlite3.connect(self.db).execute('select des from info where id = 0;'):
			return line[0]
	def getNewest(self):
		newestPage = self.webpc.get('http://www.buka.cn/category/12084/%E6%9C%80%E8%BF%91%E4%B8%8A%E6%96%B0.html')
		soup = BeautifulSoup(newestPage, 'html.parser')
		return int(common().findstr('/detail/(\d*).html', soup.select_one('#mangawrap > li > a').get('href'))[0])
	def getStart(self):
		cursor = sqlite3.connect(self.db).execute('select id from info order by id desc limit 1;')
		for line in cursor:
			return int(line[0])
	def fetch(self):
		tmpData = []
		data = []
		for i in range(self.startId, self.newestId):
			tmpData.append(i+1)
			if len(tmpData) == 400:
				data.append(tmpData)
				tmpData = []
				if len(data) == 100:
					break;
		if len(tmpData) > 0:
			data.append(tmpData)
		pool = ThreadPool(15)
		for d in data:
			pool.apply_async(self.scrapM, args=(d, ))
		pool.close()
		pool.join()
	def scrapM(self, data):
		outData = []
		for curId in data:
			curUrl = 'http://m.buka.cn/m/%d' % curId
			print(curUrl)
			curPage = self.webm.get(curUrl)
			soup = BeautifulSoup(curPage, 'html.parser')
			curTitle = soup.select_one('title').text.strip()
			if curTitle == '布卡漫画':
				curTitle = ''
				curAuthor = ''
				curDes = ''
				curImgUrl = ''
				avail = 0
			else:
				curAuthor = soup.select_one('.mangadir-glass-author').text.strip()
				curDes = soup.select_one('.description_intro').text.strip()
				curImgUrl = quote(soup.select_one('.mangadir-glass-img > img').get('src'))
				avail = 1
			outData.append((curId, curTitle, curAuthor, curDes, curImgUrl, avail))
		conn = sqlite3.connect(self.db)
		conn.executemany('insert into info values (?, ?, ?, ?, ?, ?)', outData)
		conn.execute('update info set des = "{}" where id = 0;'.format(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())))
		conn.commit()
		conn.close()

if __name__ == '__main__':
	comic = buka('buka.db')
	comic.fetch()