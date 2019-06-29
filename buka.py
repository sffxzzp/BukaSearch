# -*- coding: utf-8 -*-
import re, sqlite3
from urllib.parse import unquote

class common:
	def findstr(self, rule, string):
		find_str = re.compile(rule)
		return find_str.findall(string)
	def mstr(self, string):
		return string.encode('gbk', 'ignore').decode('gbk')

class buka:
	def search(self, string):
		conn = sqlite3.connect('buka.db')
		cursor = conn.execute("select * from info where name like '%{}%' or author like '%{}%';".format(string, string))
		outData = []
		for m in cursor:
			outData.append(m)
		self.output(string, outData)
		conn.close()
	def output(self, search, books):
		panelHtml = '<div class="dispanel"><table border="1"cellspacing="0"><tr><td rowspan="3" style="width:140px;"><img class="img"src="%(img)s"/></td><td><span class="title"><a target="_blank"href="http://www.buka.cn/detail/%(id)s.html">%(name)s</a></span><span class="app"><a target="_blank"href="buka://detail/manga/%(id)s">在App中打开</a></span></td></tr><tr><td><span class="author">作者：%(author)s</span></td></tr><tr><td><span class="description">%(des)s</span></td></tr></table></div>'
		panels = ''
		for book in books:
			panels += panelHtml % {'id': book[0], 'name': book[1], 'author': book[2], 'des': book[3], 'img': unquote(book[4])}
		outData = '<html><head><title>'+search+' - 搜索结果</title><style>a:link{text-decoration:none}.dispanel{width:96%;margin:2%}.dispanel>table{width:100%}.app{float:right}.img{width:140px}</style></head><body>'+panels+'</body></html>'
		with open('output.html', 'w', encoding='utf-8') as outfile:
			outfile.write(outData)
		print('已导出至 output.html')

if __name__ == '__main__':
	comic = buka()
	comic.search(input('请输入要搜索的内容（名称/作者）：'))