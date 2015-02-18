# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Vespa
"""


from support import *
import hashlib

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

def GetPopularVedio(begintime, endtime, sortType=TYPE_BOFANG, zone=0, page=1, original=0):
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
    return GetVedioFromRate(content)

def GetVedioFromRate(content):
"""
从视频搜索源码页面提取视频信息
"""
    #av号和标题
    regular1 = r'<a href="/video/av(\d+)/" target="_blank" class="title">([^/]+)</a>'
    info1 = GetRE(content,regular1)
    #观看数
    regular2 = r'<i class="gk" title=".*">(.+)</i>'
    info2 = GetRE(content,regular2)
    #收藏
    regular3 = r'<i class="sc" title=".*">(.+)</i>'
    info3 = GetRE(content,regular3)
    #弹幕
    regular4 = r'<i class="dm" title=".*">(.+)</i>'
    info4 = GetRE(content,regular4)
    #日期
    regular5 = r'<i class="date" title=".*">(\d+-\d+-\d+ \d+:\d+)</i>'
    info5 = GetRE(content,regular5)
    #封面
    regular6 = r'<img src="(.+)">'
    info6 = GetRE(content,regular6)
    #Up的id和名字
    regular7 = r'<a class="up r10000" href="http://space\.bilibili\.com/(\d+)" target="_blank">(.+)</a>'
    info7 = GetRE(content,regular7)
    #!!!!!!!!这里可以断言所有信息长度相等
    vedioNum = len(info1)#视频长度
    vedioList = []
    for i in range(vedioNum):
        vedio_t = Vedio()
        vedio_t.aid = getint(info1[i][0])
        vedio_t.title = info1[i][1]
        vedio_t.guankan = getint(info2[i])
        vedio_t.shoucang = getint(info3[i])
        vedio_t.danmu = getint(info4[i])
        vedio_t.date = info5[i]
        vedio_t.cover = info6[i]
        vedio_t.author = User(info7[i][0],info7[i][1])
        vedioList.append(vedio_t)
    return vedioList

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

def GetVedioOfZhuanti(spid, season_id=None, bangumi=None):
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
    vediolist = []
    for vedio_idx in jsoninfo.Getvalue('list'):
        vedio = Vedio(vedio_idx['aid'],vedio_idx['title'])
        vedio.cover = vedio_idx['cover']
        vedio.guankan = vedio_idx['click']
        if vedio_idx.has_key('episode'):
            vedio.episode = vedio_idx['episode']
        vedio.src = vedio_idx["from"]
        vedio.cid = vedio_idx["cid"]
        vedio.page = vedio_idx["page"]
        vediolist.append(vedio)
    return vediolist

def GetComment(aid, page = None, pagesize = None, ver=None, order = None):
    """
输入：
    aid：AV号
    page：页码
    pagesize：单页返回的记录条数，最大不超过300，默认为10。
    ver：API版本,最新是3
    order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序
返回：
    评论列表
    """
    url = 'http://api.bilibili.cn/feedback?aid='+GetString(aid)
    if page:
        url += '&page='+GetString(page)
    if pagesize:
        url += '&pagesize='+GetString(pagesize)
    if ver:
        url += '&ver='+GetString(ver)
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

def GetAllComment(aid, ver=None, order = None):
    """
获取一个视频全部评论，有可能需要多次爬取，所以会有较大耗时
输入：
    aid：AV号
    ver：API版本,最新是3
    order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序
返回：
    评论列表
    """
    MaxPageSize = 300
    commentList = GetComment(aid=aid,pagesize=MaxPageSize,ver=ver,order=order)
    if commentList.page == 1:
        return commentList
    for p in range(2,commentList.page+1):
        t_commentlist = GetComment(aid=aid,pagesize=MaxPageSize,page=p,ver=ver,order=order)
        for liuyan in t_commentlist.comments:
            commentList.comments.append(liuyan)
        time.sleep(0.5)
    return commentList

def GetVedioInfo(aid, appkey,page = 1, AppSecret=None, fav = None):
    paras = {'id': GetString(aid),'page': GetString(page)}
    if fav:
        paras['fav'] = fav
    url =  'http://api.bilibili.cn/view?'+GetSign(paras,appkey,AppSecret)
    jsoninfo = JsonInfo(url)
    vedio = Vedio(aid,jsoninfo.Getvalue('title'))
    vedio.guankan = jsoninfo.Getvalue('play')
    vedio.commentNumber = jsoninfo.Getvalue('review')
    vedio.danmu = jsoninfo.Getvalue('video_review')
    vedio.shoucang = jsoninfo.Getvalue('favorites')
    vedio.description = jsoninfo.Getvalue('description')
    vedio.tag = []
    taglist = jsoninfo.Getvalue('tag')
    if taglist:
        for tag in taglist.split(','):
            vedio.tag.append(tag)
    vedio.cover = jsoninfo.Getvalue('pic')
    vedio.author = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('author'))
    vedio.page = jsoninfo.Getvalue('pages')
    vedio.date = jsoninfo.Getvalue('created_at')
    vedio.credit = jsoninfo.Getvalue('credit')
    vedio.coin = jsoninfo.Getvalue('coins')
    vedio.spid = jsoninfo.Getvalue('spid')
    vedio.cid = jsoninfo.Getvalue('cid')
    vedio.offsite = jsoninfo.Getvalue('offsite')
    vedio.partname = jsoninfo.Getvalue('partname')
    vedio.src = jsoninfo.Getvalue('src')
    vedio.tid = jsoninfo.Getvalue('tid')
    vedio.typename = jsoninfo.Getvalue('typename')
    vedio.instant_server = jsoninfo.Getvalue('instant_server')
    return vedio

def GetSign(params, appkey, AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
待添加：【重要！】
    需要做URL编码并保证字母都是大写，如 %2F
    """
    params['appkey']=appkey
    data = ""
    paras = params.keys()
    paras.sort()
    for para in paras:
        if data != "":
            data += "&"
        data += para + "=" + str(params[para])
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update(data+AppSecret)
    return data+'&sign='+m.hexdigest()

def GetGangumi(appkey, btype = None, weekday = None, AppSecret=None):
    """
获取新番信息
输入：
    btype：番剧类型 2: 二次元新番 3: 三次元新番 默认：所有
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
    for bgm in jsoninfo.Getvalue('list'):
        bangumi = Bangumi()
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
        bangumilist.append(bangumi)
    return bangumilist

def biliVedioSearch(keyword, order = 'default', pagesize = 20, page = 1):
    """
根据关键词搜索视频
输入：
    order：排序方式  默认default，其余待测试
    keyword：关键词
    pagesize:返回条目多少
    page：页码
    """
    url = "http://api.bilibili.cn/search?keyword=%s&order=%s&pagesize=%d&page=%d"%(keyword, order, pagesize, page)
    jsoninfo = JsonInfo(url)
    vediolist = []
    for vedio_idx in jsoninfo.Getvalue('result'):
        if vedio_idx['type'] != 'video':
            continue
        vedio = Vedio(vedio_idx['aid'], vedio_idx['title'])
        vedio.typename = vedio_idx['typename']
        vedio.author = User(vedio_idx['mid'], vedio_idx['author'])
        vedio.acurl = vedio_idx['arcurl']
        vedio.description = vedio_idx['description']
        vedio.arcrank = vedio_idx['arcrank']
        vedio.cover = vedio_idx['pic']
        vedio.guankan = vedio_idx['play']
        vedio.danmu = vedio_idx['video_review']
        vedio.shoucang = vedio_idx['favorites']
        vedio.commentNumber = vedio_idx['review']
        vedio.date = vedio_idx['pubdate']
        vedio.tag = vedio_idx['tag'].split(',')
        vediolist.append(vedio)
    return vediolist

def biliZhuantiSearch(keyword):
    """
根据关键词搜索专题
输入：
    keyword：关键词
    """
    url = "http://api.bilibili.cn/search?keyword=%s"%(keyword)
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
    vediolist = []
    page = jsoninfo.Getvalue('pages')
    name = jsoninfo.Getvalue('name')
    for i in range(len(jsoninfo.Getvalue('list'))-1):
        idx = str(i)
        vedio = Vedio(jsoninfo.Getvalue('list',idx,'aid'),jsoninfo.Getvalue('list',idx,'title'))
        vedio.Iscopy = jsoninfo.Getvalue('list',idx,'copyright')
        vedio.tid = jsoninfo.Getvalue('list',idx,'typeid')
        vedio.typename = jsoninfo.Getvalue('list',idx,'typename')
        vedio.subtitle = jsoninfo.Getvalue('list',idx,'subtitle')
        vedio.guankan = jsoninfo.Getvalue('list',idx,'play')
        vedio.commentNumber = jsoninfo.Getvalue('list',idx,'review')
        vedio.danmu = jsoninfo.Getvalue('list',idx,'video_review')
        vedio.shoucang = jsoninfo.Getvalue('list',idx,'favorites')
        vedio.author = User(jsoninfo.Getvalue('list',idx,'mid'),jsoninfo.Getvalue('list',idx,'author'))
        vedio.description = jsoninfo.Getvalue('list',idx,'description')
        vedio.date = jsoninfo.Getvalue('list',idx,'create')
        vedio.cover = jsoninfo.Getvalue('list',idx,'pic')
        vedio.credit = jsoninfo.Getvalue('list',idx,'credit')
        vedio.coin = jsoninfo.Getvalue('list',idx,'coins')
        vedio.duration = jsoninfo.Getvalue('list',idx,'duration')
        if click_detail != None:
            vedio.play_site = jsoninfo.Getvalue('list',idx,'play_site')
            vedio.play_forward = jsoninfo.Getvalue('list',idx,'play_forward')
            vedio.play_mobile = jsoninfo.Getvalue('list',idx,'play_mobile')
        vediolist.append(vedio)
    return [page,name,vediolist]

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
    vedio = GetVedioInfo(aid,appkey,pid,AppSecret)
    cid = vedio.cid
    media_args = {'cid': cid,'quality':4}
    resp_media = getURLContent(url_get_media+GetSign(media_args,appkey,AppSecret))
    media_urls = [str(k.wholeText).strip() for i in xml.dom.minidom.parseString(resp_media.decode('utf-8', 'replace')).getElementsByTagName('durl') for j in i.getElementsByTagName('url')[:1] for k in j.childNodes if k.nodeType == 4]
    return media_urls

if __name__ == "__main__":
#    f = open('result.txt','w')
     #获取最热视频
#    vedioList = GetPopularVedio([2014,05,20],[2014,05,27],TYPE_BOFANG,0,1)
#    for vedio in vedioList:
#        print vedio.title
     #获取用户信息
    # user = GetUserInfoBymid('72960')
    # print user.name, user.DisplayRank
    # user = GetUserInfoByName('vespa')
    # print user.friend
    #获取专题视频信息
   # vediolist = GetVedioOfZhuanti('5691',bangumi=1)
   # for vedio in vediolist:
   #     print vedio.title
    #获取评论
#    commentList = GetAllComment('1154794')
#    for liuyan in commentList.comments:
#        print liuyan.lv,'-',liuyan.post_user.name,':',liuyan.msg
#    f.close()
    #获取视频信息
    # appkey = '************'
    # secretkey = None #选填
#    vedio = GetVedioInfo(1152959,appkey=appkey,AppSecret=secretkey)
#    for tag in vedio.tag:
#        print tag
    #获取新番
#    bangumilist = GetGangumi(appkey,btype = 2,weekday=1,AppSecret=secretkey)
#    for bangumi in bangumilist:
#        print bangumi.scover,bangumi.mcover,bangumi.cover
    #获取分类排行
#    [page,name,vediolist] = GetRank(appkey,tid='0',order='hot',page=12,pagesize = 100,begin=[2014,1,1],end=[2014,2,1],click_detail='true')
#    for vedio in vediolist:
#        print vedio.title,vedio.play_site
#获取弹幕
#    vedio = GetVedioInfo(1677082,appkey,AppSecret=screatekey)
#    for danmu in GetDanmuku(vedio.cid):
#        print danmu
    #获取视频下载地址列表
    # media_urls = GetBilibiliUrl('http://www.bilibili.com/video/av1691618/',appkey = appkey)
    # for url in media_urls:
    #     print(url)
    # for vedio in biliVedioSearch('rwby'):
    #     print vedio.title
    for zhuanti in biliZhuantiSearch('rwby'):
        print zhuanti.title.encode('utf8')