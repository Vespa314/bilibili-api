# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:59:09 2014

@author: Vespa
"""
import urllib2
import re
import json
import zlib
import gzip
import xml.dom.minidom

from biclass import *
import time
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
        return temp
    info = None

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
