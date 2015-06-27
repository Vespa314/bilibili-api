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
        if self.followlist:
            for fo in self.followlist:
                fid.write('\t%s\n'%fo);
#   获取空间地址
    def GetSpace(self):
        return 'http://space.bilibili.tv/'+str(self.mid);
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
    

class Video():
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
        self.author.saveToFile(fid);
        fid.write('\n');
    aid = None;
    title = None;
    guankan = None;
    shoucang = None;
    danmu = None;
    date = None;
    cover = None;
    commentNumber = None;
    description = None;
    tag = None;
    author = None;
    page = None;
    credit = None;
    coin = None;
    spid = None;
    cid = None;
    offsite = None;#Flash播放调用地址
    Iscopy = None;
    subtitle = None;
    duration = None;
    episode = None;
#不明：    
    tid = None;
    typename = None;
    instant_server = None;
    src = None;
    partname = None;
#播放信息：
    play_site = None;
    play_forward = None;
    play_mobile = None;
    
class Bangumi():
    def __init__(self):
        pass;
    typeid = None;
    lastupdate = None;
    areaid = None;
    bgmcount = None;#番剧当前总集数
    title = None;
    lastupdate_at = None;
    attention = None;
    cover = None;
    priority = None;
    area = None;
    weekday = None;
    spid = None;
    new = None;
    scover = None;
    mcover = None;
    click = None;
    season_id = None;
    
class Comment():
    def __init__(self):
        self.post_user = User();
    lv = None;#楼层
    fbid = None;#评论id
    msg = None;
    ad_check = None;#状态 (0: 正常 1: UP主隐藏 2: 管理员删除 3: 因举报删除)
    post_user = None;

class CommentList():
    def __init__(self):
        pass;
    comments = None;
    commentLen = None;
    page = None;

