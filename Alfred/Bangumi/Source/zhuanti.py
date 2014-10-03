# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""

from support import * 
import hashlib
import datetime

def GetVedioOfZhuanti(spid,season_id=None,bangumi=None):
    """
输入：
    spid:专题id
    season_id：分季ID
    bangumi：设置为1返回剧番，不设置或者设置为0返回相关视频
返回：
    视频列表，包含av号，标题，封面和观看数
    """
    url = ' http://api.bilibili.cn/spview?spid='+GetString(spid);
    if season_id != None:
        url += '&season_id='+GetString(season_id);
    if bangumi != None:
        url += '&bangumi='+GetString(bangumi);
    jsoninfo = json.loads(getURLContent(url))
    try:
        print jsoninfo['list'][0]['aid'],
    except:
        pass


query = '{query}'
# t:今天新番
# r:最近更新
# 3：三次元
# wn:查询星期n

GetVedioOfZhuanti(query,bangumi = 1)
