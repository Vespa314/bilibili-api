# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""

import sys, time, os, re
from support import * 

#常量定义

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

#常量定义结束


class User():
    def __init__(self):
        pass
    def __init__(self,m_mid,m_name):
        self.mid = m_mid;
        self.name = m_name;
    def saveToFile(self,fid):
        fid.write('\t名字:%s\n'%self.name);
        fid.write('\tid:%s\n'%self.mid);
#   获取空间地址
    def GetSpace(self):
        return 'http://space.bilibili.tv/'+str(mid);
    mid = None;
    name = None;

class Vedio():
    def __init__(self):
        pass
#   写到文件中
    def saveToFile(self,fid):
        fid.write('av号:%d\n'%self.aid);
        fid.write('标题:%s\n'%self.title);
        fid.write('观看:%d\n'%self.guankan);
        fid.write('收藏:%d\n'%self.shoucang);
        fid.write('弹幕:%d\n'%self.danmu);
        fid.write('日期:%s\n'%self.date);
        fid.write('封面地址:%s\n'%self.cover);
        fid.write('Up主:\n');
        self.po.saveToFile(fid);
        fid.write('\n');
    aid = None;
    title = None;
    guankan = None;
    shoucang = None;
    danmu = None;
    date = None;
    cover = None;
    po = None;
#从视频源码获取视频信息
def GetVedioFromRate(content):
    #av号和标题
    regular1 = r'<a href="/video/av(\d+)/" target="_blank" class="title">([^/]+)</a>';
    info1 = GetRE(content,regular1)
    #观看数
    regular2 = r'<i class="gk" title=".*">(\d+)</i>';
    info2 = GetRE(content,regular2)
    #收藏
    regular3 = r'<i class="sc" title=".*">(\d+)</i>';
    info3 = GetRE(content,regular3)
    #弹幕
    regular4 = r'<i class="dm" title=".*">(\d+)</i>';
    info4 = GetRE(content,regular4)
    #日期
    regular5 = r'<i class="date" title=".*">(\d+-\d+-\d+ \d+:\d+)</i>';
    info5 = GetRE(content,regular5)
    #封面
    regular6 = r'<img src="(.+)">';
    info6 = GetRE(content,regular6)
    #Up的id和名字
    regular7 = r'<a class="up r10000" href="http://space.bilibili.tv/(\d+)" target="_blank">(.+)</a>'
    info7 = GetRE(content,regular7)
    #!!!!!!!!这里可以断言所有信息长度相等
    vedioNum = len(info1);#视频长度
    vedioList = [];
    for i in range(vedioNum):
        vedio_t = Vedio();
        vedio_t.aid = int(info1[i][0]);
        vedio_t.title = info1[i][1];
        vedio_t.guankan = int(info2[i]);
        vedio_t.shoucang = int(info3[i]);
        vedio_t.danmu = int(info4[i]);
        vedio_t.date = info5[i];
        vedio_t.cover = info6[i];
        vedio_t.po = User(info7[i][0],info7[i][1])
        vedioList.append(vedio_t);
    return vedioList



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




if __name__ == "__main__":
    vedioList = GetPopularVedio([2014,05,20],[2014,05,27],TYPE_BOFANG,0,1)
    f = open('result.txt','w');
    for vedio in vedioList:
        vedio.saveToFile(f);
    f.close();