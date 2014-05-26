# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:59:09 2014

@author: Administrator
"""
import urllib
import urllib2
import json
import re

def GetRE(content,regexp):
    return re.findall(regexp, content)

def getURLContent(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url = url,headers = headers);   
        content = urllib2.urlopen(req).read();
        return content;
    except:
        return ""
    
def FromJson(jsondata):
    return json.loads(jsondata)