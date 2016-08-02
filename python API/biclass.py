# -*- coding: utf-8 -*-
"""
Created on Wed May 28 01:22:20 2014

@author: Vespa
"""

class User():
    def __init__(self,m_mid=None,m_name=None):
        if m_mid:
            self.mid = m_mid
        if m_name:
            if isinstance(m_name,unicode):
                m_name = m_name.encode('utf8')
            self.name = m_name
        self.isApprove = None#是否是认证账号
        self.spaceName = None
        self.sex = None
        self.rank = None
        self.avatar = None
        self.follow = None#关注好友数目
        self.fans = None#粉丝数目
        self.article = None#投稿数
        self.place = None#所在地
        self.description = None#认证用户为认证信息 普通用户为交友宣言
        self.followlist = None#关注的好友列表
        self.friend = None
        self.DisplayRank = None
        self.message = None # 承包时会返回的承保信息
#   获取空间地址
    def GetSpace(self):
        return 'http://space.bilibili.tv/'+str(self.mid)



class Video():
    def __init__(self,m_aid=None,m_title=None):
        if m_aid:
            self.aid = m_aid
        if m_title:
            if isinstance(m_title,unicode):
                m_title = m_title.encode('utf8')
            self.title = m_title
        self.guankan = None
        self.shoucang = None
        self.danmu = None
        self.date = None
        self.cover = None
        self.commentNumber = None
        self.description = None
        self.tag = None
        self.author = None
        self.page = None
        self.credit = None
        self.coin = None
        self.spid = None
        self.cid = None
        self.offsite = None#Flash播放调用地址
        self.Iscopy = None
        self.subtitle = None
        self.duration = None
        self.episode = None
        self.arcurl = None#网页地址
        self.arcrank = None#不明
        self.tid = None
        self.index = None#剧番中的集数
        self.episode_id = None
        self.typename = None
        self.online_user = None # 当前在线观看人数
        self.partition_index = None # 属于分P视频的索引
    #不明：
        self.instant_server = None
        self.src = None
        self.partname = None
        self.allow_bp = None
        self.allow_feed = None
        self.created = None
    #播放信息：
        self.play_site = None
        self.play_forward = None
        self.play_mobile = None

class Bangumi():
    def __init__(self):
        self.typeid = None
        self.lastupdate = None
        self.area = None
        self.bgmcount = None#番剧当前总集数
        self.title = None
        self.lastupdate_at = None
        self.attention = None #订阅数
        self.cover = None
        self.priority = None
        self.area = None
        self.weekday = None
        self.spid = None
        self.new = None
        self.scover = None
        self.mcover = None
        self.click = None
        self.coin = None
        self.season_id = None
        self.season_title = None
        self.click = None # 浏览数
        self.video_view = None
        self.episode_list = []
        self.tags = []
        self.isFinished = None
        self.newest_ep_id = None
        self.newest_ep_index = None

class Comment():
    def __init__(self):
        self.post_user = User()
        self.lv = None#楼层
        self.fbid = None#评论id
        self.parent_id = None #被回复留言ID
        self.msg = None
        self.ad_check = None#状态 (0: 正常 1: UP主隐藏 2: 管理员删除 3: 因举报删除)
        self.post_user = None
        self.like = None

class CommentList():
    def __init__(self):
        self.comments = None
        self.commentLen = None
        self.page = None

class ZhuantiInfo():
    def __init__(self, m_spid,m_title):
        self.spid = m_spid
        if isinstance(m_title,unicode):
            m_title = m_title.encode('utf8')
        self.title = None
        self.author = None
        self.cover = None
        self.thumb = None
        self.ischeck = None #不明
        self.typeurl = None #总是"http://www.bilibili.com"
        self.tag = None
        self.description = None
        self.pubdate = None # 不明
        self.postdate = None
        self.lastupdate = None
        self.click = None
        self.favourite = None
        self.attention = None
        self.count = None
        self.bgmcount = None
        self.spcount = None
        self.season_id = None
        self.is_bangumi = None
        self.arcurl = None
        self.is_bangumi_end = None

class Danmu():
    def __init__(self):
        self.t_video = None
        self.t_stamp = None
        self.mid_crc = None  # 值为:hex(binascii.crc32(mid))
        self.danmu_type = None # 1:滚动弹幕 5：顶端弹幕  4：底部弹幕
        self.content = None
        self.danmu_color = None
        self.danmu_fontsize = None

class SponsorInfo():
    def __init__(self):
        self.bp = None  ## 剧番总B币
        self.percent = None  #承包总比例，不知道什么鬼
        self.ep_bp = None  ## 该话的B币
        self.ep_percent = None  ## 不明
        self.sponsor_num = None   ## 承包人数
        self.sponsor_user = None  ## 承包人列表

class LivingInfo():
    def __init__(self):
        self.url = None
        self.title = None
        self.cover = None
        self.mid = None