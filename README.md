##B站API收集整理及开发，测试【开发中】
============

### 目录：
* python API/：python版本API
* bilibili-po/：测试爬取B站up的关注关系网，以便后期分析【已完成】
  * bilibili-po/爬取结果:爬取的原始数据，包括每一个up的id，昵称，投稿数，粉丝数以及关注列表
  * bilibili-po/分析：分析爬取的数据的python代码和Mathematica代码
* bilibili-video/:爬取B站所有视频信息【已完成，数据暂不公开】
* bili-monitor/:监视B站新番各种数据脚本【已完成】
* Alfred/:几个基于此API开发的Workflow，此处不再更新，具体参见[Github](https://github.com/Vespa314/AlfredWorkFlows)【已完成】
* GetDanmuAss/：通过输入av号获得本地弹幕播放用的ASS文件【已完成】
	* spview danmaku/:批量获取专题弹幕文件【已完成】
* GetVideoUrl/：输入视频URL地址获得下载URL（改造自[biligrab](https://github.com/m13253/biligrab-danmaku2ass)】）【已完成】
* BiliMerge/：随手写的合并来自B站手机客户端离线下载的视频【已完成】
* danmu-Delay/：随手写的弹幕字幕文件延时。。【已完成】
* bili_live_guaji/:直播经验挂机脚本【已完成】

### 文件：
* api.md   ：API的详细说明
* README.md：return this

###主要三部分API组成：
* 根据爬取页面获取到的信息：
  * 视频排行【已完成】
  * 根据条件筛选视频
  * 按年份月份获取动画新番信息
* 无需认证的API接口获取：
  * 获取各个板块本周最火视频
  * 读取视频评论【已完成】
  * 读取专题信息
  * 获取专题视频信息【已完成】
  * 获取用户信息【已完成】
* 需要appkey才可以获得的信息：
  * 获取视频信息【已完成】
  * 获取新番信息【已完成】
  * 获取排行视频信息【已完成】
  * ...

###类接口：

####用户类：
```python
class User():
    def __init__(self,m_mid=None,m_name=None):
        if m_mid:
            self.mid = m_mid;
        if m_name:
            self.name = m_name;
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
```

####视频类：
```python
class Video():
    def __init__(self,m_aid=None,m_title=None):
        if m_aid:
            self.aid = m_aid;
        if m_title:
            self.title = m_title;
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
    arcurl = None;#网页地址
    arcrank = None;#不明
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
```

####评论类：
```
class Comment():
    def __init__(self):
        self.post_user = User();
    lv = None;#楼层
    fbid = None;#评论id
    msg = None;
    ad_check = None;#状态 (0: 正常 1: UP主隐藏 2: 管理员删除 3: 因举报删除)
    post_user = None;
```

####评论组(一组评论):
```
class CommentList():
    def __init__(self):
        pass;
    comments = None;
    commentLen = None;
    page = None;
```

####新番类：
```
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
```

专题类
```
class ZhuantiInfo():
    def __init__(self, m_spid,m_title):
        self.spid = m_spid
        self.title = m_title
    spid = None
    title = None
    author = None
    cover = None
    thumb = None
    ischeck = None #不明
    typeurl = None #总是”http://www.bilibili.com”
    tag = None
    description = None
    pubdate = None # 不明
    postdate = None
    lastupdate = None
    click = None
    favorite = None
    attention = None
    count = None
    bgmcount = None
    spcount = None
    season_id = None
    is_bangumi = None
    arcurl = None
```

弹幕类:
```
class Danmu():
    def __init__(self):
        pass
    t_video = None
    t_stamp = None
    mid_crc = None  # 值为:hex(binascii.crc32(mid))
    danmu_type = None # 1:滚动弹幕 5：顶端弹幕  4：底部弹幕
    content = None
    danmu_color = None
```