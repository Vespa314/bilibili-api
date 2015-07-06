# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:59:09 2014

@author: Vespa
"""
import urllib2
import urllib
import re
import json
import zlib
import gzip
import xml.dom.minidom
import hashlib
from biclass import *
import time
import sys
import os
from GetAssDanmaku import *
def GetRE(content,regexp):
    return re.findall(regexp, content)

def getURLContent(url):
    while True:
        flag = 1
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows U Windows NT 6.1 en-US rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(url = url,headers = headers)
            content = urllib2.urlopen(req).read()
        except:
        	flag = 0
        	time.sleep(5)
        if flag == 1:
        	break
    return content

class JsonInfo():
    def __init__(self,url):
        self.info = json.loads(getURLContent(url))
        if self.info.has_key('code') and self.info['code'] != 0:
            if self.info.has_key('message'):
                print "【Error】code=%d, msg=%s, url=%s"%(self.info['code'],self.Getvalue('message'),url)
            elif self.info.has_key('error'):
                print "【Error】code=%d, msg=%s, url=%s"%(self.info['code'],self.Getvalue('error'),url)
            error = True
    def Getvalue(self,*keys):
        if len(keys) == 0:
            return None
        if self.info.has_key(keys[0]):
            temp = self.info[keys[0]]
        else:
            return None
        if len(keys) > 1:
            for key in keys[1:]:
                if temp.has_key(key):
                    temp = temp[key]
                else:
                    return None
        if isinstance(temp,unicode):
            temp = temp.encode('utf8')
        return temp
    info = None
    error = False

def GetString(t):
    if type(t) == int:
        return str(t)
    return t

def getint(string):
    try:
        i = int(string)
    except:
        i = 0
    return i

def DictDecode2UTF8(dict):
    for keys in dict:
        if isinstance(dict[keys],unicode):
            dict[keys] = dict[keys].encode('utf8')
    return dict

def GetVideoFromRate(content):
    """
从视频搜索源码页面提取视频信息
    """
    #av号和标题
    regular1 = r'<a href="/video/av(\d+)/" target="_blank" class="title" [^>]*>([^/]+)</a>'
    info1 = GetRE(content,regular1)
    #观看数
    regular2 = r'<i class="gk" title=".*" [^>]*>(.+)</i>'
    info2 = GetRE(content,regular2)
    #收藏
    regular3 = r'<i class="sc" title=".*" [^>]*>(.+)</i>'
    info3 = GetRE(content,regular3)
    #弹幕
    regular4 = r'<i class="dm" title=".*" [^>]*>(.+)</i>'
    info4 = GetRE(content,regular4)
    #日期
    regular5 = r'<i class="date" title=".*">(\d+-\d+-\d+ \d+:\d+)</i>'
    info5 = GetRE(content,regular5)
    #封面
    regular6 = r'<img src="(.+)" [^>]*>'
    info6 = GetRE(content,regular6)
    #Up的id和名字
    regular7 = r'<i class="up r10000">(.*)</i>'
    info7 = GetRE(content,regular7)
    #!!!!!!!!这里可以断言所有信息长度相等
    videoNum = len(info1)#视频长度
    videoList = []
    for i in range(videoNum):
        video_t = Video()
        video_t.aid = getint(info1[i][0])
        video_t.title = info1[i][1]
        video_t.guankan = getint(info2[i])
        video_t.shoucang = getint(info3[i])
        video_t.danmu = getint(info4[i])
        video_t.date = info5[i]
        video_t.cover = info6[i]
        video_t.author = User(info7[i][0],info7[i][1])
        videoList.append(video_t)
    return videoList

def GetSign(params, appkey, AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
    """
    params['appkey']=appkey
    data = ""
    paras = params.keys()
    paras.sort()
    data = urllib.urlencode(params)
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update(data+AppSecret)
    return data+'&sign='+m.hexdigest()

def ParseComment(danmu):
    dom = xml.dom.minidom.parseString(danmu)
    comment_element = dom.getElementsByTagName('d')
    for i, comment in enumerate(comment_element):
        p = str(comment.getAttribute('p')).split(',')
        if len(comment.childNodes) != 0:
            c = str(comment.childNodes[0].wholeText).replace('/n', '\n')
        else:
            c = ""
        yield (float(p[0]),c)