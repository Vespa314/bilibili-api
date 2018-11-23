#encoding=utf-8
from urllib import request
import requests
import html3
import re
import time
import datetime as dt
def GetHtml():
	url = "https://www.bilibili.com/newlist.html"
	data = request.urlopen(url).read().decode()
	return data
def GetLatestAid(data):
	html = GetHtml()
	pattern = re.compile('<a href="/video/av(.*?)/" target="_blank" class="preview"')
	item = re.findall(pattern,html)
	item.sort(reverse=True)
	print(item[0])
	# return item[0]
if __name__ == '__main__':
	# prev = []
	# i = 1
	# prev[i] = 0
	while True:
		print(GetLatestAid(GetHtml()))
		# print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),GetLatestAid(GetHtml()))
		# prev.append(GetLatestAid(GetHtml()))
		# if len(prev) == 1:
		# 	print(prev[len(prev)-1])
		# elif len(prev) >= 2:
		# 	print(prev[1],int(prev[1])-int(prev[0]))
		# i = i + 1
		# time.sleep(1)
