# -*- coding: utf-8 -*-
"""
Created on Wed May 28 01:22:20 2014

@author: Administrator
"""

class User():
    def __init__(self,m_mid=None,m_name=None):
        if m_mid:
            self.mid = m_mid;
        if m_name:
            self.name = m_name;
    def saveToFile(self,fid):
        fid.write('名字:%s\n'%self.name);
        fid.write('id:%s\n'%self.mid);
        fid.write('是否认证:%s\n'%self.isApprove);
        fid.write('空间:%s\n'%self.spaceName);
        fid.write('性别:%s\n'%self.sex);
        fid.write('账号显示标识:%s\n'%self.rank);
        fid.write('头像:%s\n'%self.avatar);
        fid.write('关注好友数目:%d\n'%self.follow);
        fid.write('粉丝数目:%d\n'%self.fans);
        fid.write('投稿数:%d\n'%self.article);
        fid.write('地点:%s\n'%self.place);
        fid.write('认证信息:%s\n'%self.description);
        fid.write('关注好友：\n');
        for fo in self.followlist:
            fid.write('\t%s\n'%fo);
#   获取空间地址
    def GetSpace(self):
        return 'http://space.bilibili.tv/'+str(mid);
    mid = None;
    name = None;
    isApprove = False;#是否是认证账号
    spaceName = "";
    sex = ""
    rank = None;
    avatar = None;
    follow = 0;#关注好友数目
    fans = 0;#粉丝数目
    article = 0;#投稿数
    place = None;#所在地
    description = None;#认证用户为认证信息 普通用户为交友宣言
    followlist = None;#关注的好友列表
    

class Vedio():
    def __init__(self,m_aid=None,m_title=None):
        if m_aid:
            self.aid = m_aid;
        if m_title:
            self.title = m_title;
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