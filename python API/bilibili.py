# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""

import sys, time, os, re
from support import * 

############################常量定义

#####排序方式
#收藏
TYPE_SHOUCANG = 'stow'
#评论数
TYPE_PINGLUN = 'review'
#播放数
TYPE_BOFANG = 'hot'
#硬币数
TYPE_YINGBI = 'promote'
#用户评分
TYPE_PINGFEN = 'comment'
#弹幕数
TYPE_DANMU = 'damku'
#拼音
TYPE_PINYIN = 'pinyin'
#投稿时间
TYPE_TOUGAO = 'default'
############################常量定义结束

def GetPopularVedio(begintime,endtime,sortType=TYPE_BOFANG,zone=0,page=1,original=0):
    """
输入：    
    begintime：起始时间，三元数组[year1,month1,day1]
    endtime：终止时间,三元数组[year2,month2,day2]
    sortType：字符串，排序方式，参照TYPE_开头的常量
    zone:整数，分区，参照api.md文档说明
    page：整数，页数
    
返回：
    视频列表,包含AV号，标题，观看数，收藏数，弹幕数，投稿日期，封面，UP的id号和名字
备注：
    待添加：保证时间小于三个月
    待添加：TYPE_PINYIN模式后面要添加类似：TYPE_PINYIN-'A'
    待添加：TYPE_PINYIN和TYPE_TOUGAO情况下zone不可以等于[0,1,3,4,5,36,11,13]
    """
    #判断是否原创    
    if original:
        ori = '-original';
    else:
        ori = ''
    url = 'http://www.bilibili.tv/list/%s-%d-%d-%d-%d-%d~%d-%d-%d%s.html'%(sortType,zone,page,begintime[0],begintime[1],begintime[2],endtime[0],endtime[1],endtime[2],ori);    
    content = getURLContent(url);
    return GetVedioFromRate(content);

def GetUserInfo(url):
    """
由GetUserInfoBymid(mid)或者GetUserInfoByName(name)调用
返回：
    用户信息
待添加：
    如果用户不存在返回的是：{"code":-626,"message":"User is not exists."}
    """
    content = getURLContent(url)
    jsoninfo = FromJson(content);
    user = User(jsoninfo['mid'],jsoninfo['name'].encode('utf8'));
    user.isApprove = jsoninfo['approve'];
    user.spaceName = jsoninfo['spacename'].encode('utf8');
    user.sex = jsoninfo['sex'].encode('utf8');
    user.rank = jsoninfo['rank'];
    user.avatar = jsoninfo['face'];
    user.follow = jsoninfo['attention'];
    user.fans = jsoninfo['fans'];
    user.article = jsoninfo['article'];
    user.place = jsoninfo['place'];
    user.description = jsoninfo['description'];
    user.followlist = [];
    for fo in jsoninfo['attentions']:
        user.followlist.append(jsoninfo['attentions'][fo])
    return user;

def GetUserInfoBymid(mid):
    """
输入：
    mid：查询的用户的id
返回：
    查看GetUserInfo()函数
    """
    mid = GetString(mid);
    url = 'http://api.bilibili.cn/userinfo'+"?mid="+mid;
    return GetUserInfo(url)
    
def GetUserInfoByName(name):
    """
输入：
    mid：查询的用户的昵称
返回：
    查看GetUserInfo()函数
    """
    name = GetString(name);
    url = 'http://api.bilibili.cn/userinfo'+"?user="+name;
    print url
    return GetUserInfo(url)

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
    content = getURLContent(url)
    jsoninfo = FromJson(content);
    vediolist = [];
    for vedio_idx in jsoninfo['list']:
        vedio = Vedio(jsoninfo['list'][vedio_idx]['aid'],jsoninfo['list'][vedio_idx]['title']);
        vedio.cover = jsoninfo['list'][vedio_idx]['cover'];
        vedio.guankan = jsoninfo['list'][vedio_idx]['click'];
        vediolist.append(vedio);
    return vediolist

if __name__ == "__main__":
#     f = open('result.txt','w');
     
#    vedioList = GetPopularVedio([2014,05,20],[2014,05,27],TYPE_BOFANG,0,1)
#    for vedio in vedioList:
#        vedio.saveToFile(f);
     
#     user = GetUserInfoBymid('72960');
#     print user.name.decode('utf8','ignore').encode('gbk','ignore')
#     user = GetUserInfoByName('vespa')
#     print user.spaceName.decode('utf8','ignore').encode('gbk','ignore')
##    user.saveToFile(f);    
    
#    vediolist = GetVedioOfZhuanti('6492',bangumi=0);
#    for vedio in vediolist:
#        print vedio.title
#     f.close();