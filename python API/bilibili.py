# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Vespa
"""


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

def GetPopularVideo(begintime, endtime, sortType=TYPE_BOFANG, zone=0, page=1, original=0):
    """
输入：
    begintime：起始时间，三元数组[year1,month1,day1]
    endtime：终止时间,三元数组[year2,month2,day2]
    sortType：字符串，排序方式，参照TYPE_开头的常量
    zone:整数，分区，参照api.md文档说明
    page：整数，页数
返回：
    视频列表,包含AV号，标题，观看数，收藏数，弹幕数，投稿日期，封面，UP的id号和名字
    """
    # TYPE_PINYIN和TYPE_TOUGAO情况下zone不可以等于[0,1,3,4,5,36,11,13]
    if sortType in [TYPE_PINYIN,TYPE_TOUGAO]:
        if zone in [0,1,3,4,5,36,11,13]:
            return []
    #判断是否原创
    if original:
        ori = '-original'
    else:
        ori = ''
    url = 'http://www.bilibili.tv/list/%s-%d-%d-%d-%d-%d~%d-%d-%d%s.html'%(sortType,zone,page,begintime[0],begintime[1],begintime[2],endtime[0],endtime[1],endtime[2],ori)
    content = getURLContent(url)
    return GetVideoFromRate(content)


def GetUserInfo(url):
    """
由GetUserInfoBymid(mid)或者GetUserInfoByName(name)调用
返回：
    用户信息
待添加：
    如果用户不存在返回的是：{"code":-626,"message":"User is not exists."}
    """
    jsoninfo = JsonInfo(url)
    user = User(jsoninfo.Getvalue('mid'), jsoninfo.Getvalue('name'))
    user.isApprove = jsoninfo.Getvalue('approve')
    #b站现在空间名暂时不返回
    #user.spaceName = jsoninfo.Getvalue('spacename')
    user.sex = jsoninfo.Getvalue('sex')
    user.rank = jsoninfo.Getvalue('rank')
    user.avatar = jsoninfo.Getvalue('face')
    user.follow = jsoninfo.Getvalue('attention')
    user.fans = jsoninfo.Getvalue('fans')
    user.article = jsoninfo.Getvalue('article')
    user.place = jsoninfo.Getvalue('place')
    user.description = jsoninfo.Getvalue('description')
    user.friend = jsoninfo.Getvalue('friend')
    user.DisplayRank = jsoninfo.Getvalue('DisplayRank')
    user.followlist = []
    for fo in jsoninfo.Getvalue('attentions'):
        user.followlist.append(fo)
    return user

def GetUserInfoBymid(mid):
    """
输入：
    mid：查询的用户的id
返回：
    查看GetUserInfo()函数
    """
    mid = GetString(mid)
    url = 'http://api.bilibili.cn/userinfo'+"?mid="+mid
    return GetUserInfo(url)

def GetUserInfoByName(name):
    """
输入：
    mid：查询的用户的昵称
返回：
    查看GetUserInfo()函数
    """
    name = GetString(name)
    url = 'http://api.bilibili.cn/userinfo'+"?user="+name
    return GetUserInfo(url)

def GetVideoOfZhuanti(spid, season_id=None, bangumi=None):
    """
输入：
    spid:专题id
    season_id：分季ID
    bangumi：设置为1返回剧番，不设置或者设置为0返回相关视频
返回：
    视频列表，包含av号，标题，封面和观看数
    """
    url = ' http://api.bilibili.cn/spview?spid='+GetString(spid)
    if season_id:
        url += '&season_id='+GetString(season_id)
    if bangumi:
        url += '&bangumi='+GetString(bangumi)
    jsoninfo = JsonInfo(url)
    videolist = []
    for video_idx in jsoninfo.Getvalue('list'):
        video = Video(video_idx['aid'],video_idx['title'])
        video.cover = video_idx['cover']
        video.guankan = video_idx['click']
        if video_idx.has_key('episode'):
            video.episode = video_idx['episode']
        video.src = video_idx["from"]
        video.cid = video_idx["cid"]
        video.page = video_idx["page"]
        videolist.append(video)
    return videolist

def GetComment(aid, page = None, pagesize = None, order = None):
    """
输入：
    aid：AV号
    page：页码
    pagesize：单页返回的记录条数，最大不超过300，默认为10。
    order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序
返回：
    评论列表
    """
    url = 'http://api.bilibili.cn/feedback?aid='+GetString(aid)
    if page:
        url += '&page='+GetString(page)
    if pagesize:
        url += '&pagesize='+GetString(pagesize)
    if order:
        url += '&order='+GetString(order)
    jsoninfo = JsonInfo(url)
    commentList = CommentList()
    commentList.comments = []
    commentList.commentLen = jsoninfo.Getvalue('totalResult')
    commentList.page = jsoninfo.Getvalue('pages')
    idx = 0
    while jsoninfo.Getvalue(str(idx)):
        liuyan = Comment()
        liuyan.lv = jsoninfo.Getvalue(str(idx),'lv')
        liuyan.fbid = jsoninfo.Getvalue(str(idx),'fbid')
        liuyan.msg = jsoninfo.Getvalue(str(idx),'msg')
        liuyan.ad_check = jsoninfo.Getvalue(str(idx),'ad_check')
        liuyan.post_user.mid = jsoninfo.Getvalue(str(idx),'mid')
        liuyan.post_user.avatar = jsoninfo.Getvalue(str(idx),'face')
        liuyan.post_user.rank = jsoninfo.Getvalue(str(idx),'rank')
        liuyan.post_user.name = jsoninfo.Getvalue(str(idx),'nick')
        commentList.comments.append(liuyan)
        idx += 1
    return commentList

def GetAllComment(aid, order = None):
    """
获取一个视频全部评论，有可能需要多次爬取，所以会有较大耗时
输入：
    aid：AV号
    order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序
返回：
    评论列表
    """
    MaxPageSize = 300
    commentList = GetComment(aid=aid, pagesize=MaxPageSize, order=order)
    if commentList.page == 1:
        return commentList
    for p in range(2,commentList.page+1):
        t_commentlist = GetComment(aid=aid,pagesize=MaxPageSize,page=p,ver=ver,order=order)
        for liuyan in t_commentlist.comments:
            commentList.comments.append(liuyan)
        time.sleep(0.5)
    return commentList

def GetVideoInfo(aid, appkey,page = 1, AppSecret=None, fav = None):
    """
获取视频信息
输入：
    aid：AV号
    page：页码
    fav：是否读取会员收藏状态 (默认 0)
    """
    paras = {'id': GetString(aid),'page': GetString(page)}
    if fav:
        paras['fav'] = fav
    url =  'http://api.bilibili.cn/view?'+GetSign(paras,appkey,AppSecret)
    jsoninfo = JsonInfo(url)
    video = Video(aid,jsoninfo.Getvalue('title'))
    video.guankan = jsoninfo.Getvalue('play')
    video.commentNumber = jsoninfo.Getvalue('review')
    video.danmu = jsoninfo.Getvalue('video_review')
    video.shoucang = jsoninfo.Getvalue('favorites')
    video.description = jsoninfo.Getvalue('description')
    video.tag = []
    taglist = jsoninfo.Getvalue('tag')
    if taglist:
        for tag in taglist.split(','):
            video.tag.append(tag)
    video.cover = jsoninfo.Getvalue('pic')
    video.author = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('author'))
    video.page = jsoninfo.Getvalue('pages')
    video.date = jsoninfo.Getvalue('created_at')
    video.credit = jsoninfo.Getvalue('credit')
    video.coin = jsoninfo.Getvalue('coins')
    video.spid = jsoninfo.Getvalue('spid')
    video.cid = jsoninfo.Getvalue('cid')
    video.offsite = jsoninfo.Getvalue('offsite')
    video.partname = jsoninfo.Getvalue('partname')
    video.src = jsoninfo.Getvalue('src')
    video.tid = jsoninfo.Getvalue('tid')
    video.typename = jsoninfo.Getvalue('typename')
    video.instant_server = jsoninfo.Getvalue('instant_server')
    ## 以下三个意义不明。。
    # video.allow_bp = jsoninfo.Getvalue('allow_bp')
    # video.allow_feed = jsoninfo.Getvalue('allow_feed')
    # video.created = jsoninfo.Getvalue('created')
    return video


def GetBangumi(appkey, btype = None, weekday = None, AppSecret=None):
    """
获取新番信息
输入：
    btype：番剧类型 2: 二次元新番 3: 三次元新番 默认(0)：所有
    weekday:周一:1 周二:2 ...周六:6
    """
    paras = {}
    if btype != None and btype in [2,3]:
        paras['btype'] = GetString(btype)
    if weekday != None:
        paras['weekday'] = GetString(weekday)
    url =  'http://api.bilibili.cn/bangumi?' + GetSign(paras, appkey, AppSecret)
    jsoninfo = JsonInfo(url)
    bangumilist = []
    if jsoninfo.Getvalue('code') != 0:
        print jsoninfo.Getvalue('error')
        return bangumilist
    for bgm in jsoninfo.Getvalue('list'):
        bangumi = Bangumi()
        bgm = DictDecode2UTF8(bgm)
        bangumi.typeid = bgm['typeid']
        bangumi.lastupdate = bgm['lastupdate']
        bangumi.areaid = bgm['areaid']
        bangumi.bgmcount = getint(bgm['bgmcount'])
        bangumi.title = bgm['title']
        bangumi.lastupdate_at = bgm['lastupdate_at']
        bangumi.attention = bgm['attention']
        bangumi.cover = bgm['cover']
        bangumi.priority = bgm['priority']
        bangumi.area = bgm['area']
        bangumi.weekday = bgm['weekday']
        bangumi.spid = bgm['spid']
        bangumi.new = bgm['new']
        bangumi.scover = bgm['scover']
        bangumi.mcover = bgm['mcover']
        bangumi.click = bgm['click']
        bangumi.season_id = bgm['season_id']
        bangumi.click = bgm['click']
        bangumi.video_view = bgm['video_view']
        bangumilist.append(bangumi)
    return bangumilist

def biliVideoSearch(appkey, AppSecret, keyword, order = 'default', pagesize = 20, page = 1):
    """
【注】：
    旧版Appkey不可用，必须配合AppSecret使用！！

根据关键词搜索视频
输入：
    order：排序方式  默认default，其余待测试
    keyword：关键词
    pagesize:返回条目多少
    page：页码
    """
    paras = {}
    paras['keyword'] = GetString(keyword)
    paras['order'] = GetString(order)
    paras['pagesize'] = GetString(pagesize)
    paras['page'] = GetString(page)
    url =  'http://api.bilibili.cn/search?' + GetSign(paras, appkey, AppSecret)
    jsoninfo = JsonInfo(url)
    videolist = []
    for video_idx in jsoninfo.Getvalue('result'):
        if video_idx['type'] != 'video':
            continue
        video = Video(video_idx['aid'], video_idx['title'])
        video.typename = video_idx['typename']
        video.author = User(video_idx['mid'], video_idx['author'])
        video.acurl = video_idx['arcurl']
        video.description = video_idx['description']
        video.arcrank = video_idx['arcrank']
        video.cover = video_idx['pic']
        video.guankan = video_idx['play']
        video.danmu = video_idx['video_review']
        video.shoucang = video_idx['favorites']
        video.commentNumber = video_idx['review']
        video.date = video_idx['pubdate']
        video.tag = video_idx['tag'].split(',')
        videolist.append(video)
    return videolist

def biliZhuantiSearch(appkey, AppSecret, keyword):
    """
根据关键词搜索专题
输入：
    keyword：关键词
    """
    paras = {}
    paras['keyword'] = GetString(keyword)
    url = 'http://api.bilibili.cn/search?' + GetSign(paras, appkey, AppSecret)
    jsoninfo = JsonInfo(url)
    zhuantiList = []
    for zhuanti_idx in jsoninfo.Getvalue('result'):
        if zhuanti_idx['type'] != 'special':
            continue
        zhuanti = ZhuantiInfo(zhuanti_idx['spid'], zhuanti_idx['title'])
        zhuanti.author = User(zhuanti_idx['mid'], zhuanti_idx['author'])
        zhuanti.cover = zhuanti_idx['pic']
        zhuanti.thumb = zhuanti_idx['thumb']
        zhuanti.ischeck = zhuanti_idx['ischeck']
        zhuanti.tag = zhuanti_idx['tag'].split(',')
        zhuanti.description = zhuanti_idx['description']
        zhuanti.pubdate = zhuanti_idx['pubdate']
        zhuanti.postdate = zhuanti_idx['postdate']
        zhuanti.lastupdate = zhuanti_idx['lastupdate']
        zhuanti.click = zhuanti_idx['click']
        zhuanti.favourite = zhuanti_idx['favourite']
        zhuanti.attention = zhuanti_idx['attention']
        zhuanti.count = zhuanti_idx['count']
        zhuanti.bgmcount = zhuanti_idx['bgmcount']
        zhuanti.spcount = zhuanti_idx['spcount']
        zhuanti.season_id = zhuanti_idx['season_id']
        zhuanti.is_bangumi = zhuanti_idx['is_bangumi']
        zhuanti.arcurl = zhuanti_idx['arcurl']
        zhuantiList.append(zhuanti)
    return zhuantiList

#def GetBangumiByTime(year, month):
#    url='http://www.bilibili.tv/index/bangumi/%s-%s.json'%(GetString(year),GetString(month))
#    print url
#    jsoninfo = getURLContent(url)
#    print jsoninfo

def GetRank(appkey, tid, begin=None, end=None, page = None, pagesize=None, click_detail =None, order = None, AppSecret=None):
    """
获取排行信息
输入：
    详见https://github.com/Vespa314/bilibili-api/blob/master/api.md
输出：
    详见https://github.com/Vespa314/bilibili-api/blob/master/api.md
    """
    paras = {}
    paras['appkey']=appkey
    paras['tid']=GetString(tid)
    if order:
        paras['order']=order
    if click_detail:
        paras['click_detail']=click_detail
    if pagesize:
        paras['pagesize']=GetString(pagesize)
    if begin != None and len(begin)==3:
        paras['begin']='%d-%d-%d'%(begin[0],begin[1],begin[2])
    if end != None and len(end)==3:
        paras['end']='%d-%d-%d'%(end[0],end[1],end[2])
    if page:
        paras['page']=GetString(page)
    if click_detail:
        paras['click_detail'] = click_detail
    url = 'http://api.bilibili.cn/list?' + GetSign(paras,appkey,AppSecret)
    jsoninfo = JsonInfo(url)
    videolist = []
    if jsoninfo.Getvalue('code') != 0:
        print jsoninfo.Getvalue('error')
        return videolist
    page = jsoninfo.Getvalue('pages')
    name = jsoninfo.Getvalue('name')
    for i in range(len(jsoninfo.Getvalue('list'))-1):
        idx = str(i)
        video = Video(jsoninfo.Getvalue('list',idx,'aid'),jsoninfo.Getvalue('list',idx,'title'))
        video.Iscopy = jsoninfo.Getvalue('list',idx,'copyright')
        video.tid = jsoninfo.Getvalue('list',idx,'typeid')
        video.typename = jsoninfo.Getvalue('list',idx,'typename')
        video.subtitle = jsoninfo.Getvalue('list',idx,'subtitle')
        video.guankan = jsoninfo.Getvalue('list',idx,'play')
        # video.commentNumber = jsoninfo.Getvalue('list',idx,'review')
        video.danmu = jsoninfo.Getvalue('list',idx,'video_review')
        video.shoucang = jsoninfo.Getvalue('list',idx,'favorites')
        video.author = User(jsoninfo.Getvalue('list',idx,'mid'),jsoninfo.Getvalue('list',idx,'author'))
        video.description = jsoninfo.Getvalue('list',idx,'description')
        video.date = jsoninfo.Getvalue('list',idx,'create')
        video.cover = jsoninfo.Getvalue('list',idx,'pic')
        video.credit = jsoninfo.Getvalue('list',idx,'credit')
        video.coin = jsoninfo.Getvalue('list',idx,'coins')
        video.commentNumber = jsoninfo.Getvalue('list',idx,'comment')
        video.duration = jsoninfo.Getvalue('list',idx,'duration')
        if click_detail != None:
            video.play_site = jsoninfo.Getvalue('list',idx,'play_site')
            video.play_forward = jsoninfo.Getvalue('list',idx,'play_forward')
            video.play_mobile = jsoninfo.Getvalue('list',idx,'play_mobile')
        videolist.append(video)
    return [page,name,videolist]

def GetDanmuku(cid):
    cid = getint(cid)
    url = "http://comment.bilibili.cn/%d.xml"%(cid)
    content = zlib.decompressobj(-zlib.MAX_WBITS).decompress(getURLContent(url))
    content = GetRE(content,r'<d p=[^>]*>([^<]*)<')
    return content

def GetBilibiliUrl(url, appkey, AppSecret=None):
    overseas=False
    url_get_media = 'http://interface.bilibili.com/playurl?' if not overseas else 'http://interface.bilibili.com/v_cdn_play?'
    regex_match = re.findall('http:/*[^/]+/video/av(\\d+)(/|/index.html|/index_(\\d+).html)?(\\?|#|$)',url)
    if not regex_match:
        return []
    aid = regex_match[0][0]
    pid = regex_match[0][2] or '1'
    video = GetVideoInfo(aid,appkey,pid,AppSecret)
    cid = video.cid
    media_args = {'cid': cid,'quality':4}
    resp_media = getURLContent(url_get_media+GetSign(media_args,appkey,AppSecret))
    media_urls = [str(k.wholeText).strip() for i in xml.dom.minidom.parseString(resp_media.decode('utf-8', 'replace')).getElementsByTagName('durl') for j in i.getElementsByTagName('url')[:1] for k in j.childNodes if k.nodeType == 4]
    return media_urls

if __name__ == "__main__":
    #获取最热视频
    # videoList = GetPopularVideo([2014,05,20],[2014,05,27],TYPE_BOFANG,0,1)
    # for video in videoList:
    #     print video.title
     #获取用户信息
    # user = GetUserInfoBymid('72960')
    # print user.name,user.DisplayRank
    # user = GetUserInfoByName('vespa')
    # print user.friend
    #获取专题视频信息
    # videolist = GetVideoOfZhuanti('46465',bangumi=1)
    # for video in videolist:
    #     print video.title
    #获取评论
    # commentList = GetAllComment('1154794')
    # for liuyan in commentList.comments:
    #     print liuyan.lv,'-',liuyan.post_user.name,':',liuyan.msg
    #获取视频信息
    # appkey = '************'
    # secretkey = None #选填
    # video = GetVideoInfo(1152959,appkey=appkey,AppSecret=secretkey)
    # for tag in video.tag:
    #     print tag
    #获取新番
    # bangumilist = GetBangumi(appkey,btype = 2,weekday=1,AppSecret=secretkey)
    # for bangumi in bangumilist:
    #     print bangumi.title
    #获取分类排行
    # [page,name,videolist] = GetRank(appkey,tid='0',order='hot',page=1,pagesize = 100,begin=[2014,1,1],end=[2014,2,1],click_detail='true')
    # for video in videolist:
    #     print video.title,video.play_site
    #获取弹幕
    # video = GetVideoInfo(1677082,appkey,AppSecret=secretkey)
    # for danmu in GetDanmuku(video.cid):
    #     print danmu
    #获取视频下载地址列表
    # media_urls = GetBilibiliUrl('http://www.bilibili.com/video/av1691618/',appkey = appkey)
    # for url in media_urls:
    #     print(url)
    #视频搜索
    # for video in biliVideoSearch(appkey,secretkey,'rwby'):
    #     print video.title
    #专题搜索
    # for zhuanti in biliZhuantiSearch(appkey,secretkey,'rwby'):
    #     print zhuanti.title