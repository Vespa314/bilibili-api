# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
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
    jsoninfo = JsonInfo(url);
    user = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('name').encode('utf8'));
    user.isApprove = jsoninfo.Getvalue('approve');
    user.spaceName = jsoninfo.Getvalue('spacename').encode('utf8');
    user.sex = jsoninfo.Getvalue('sex').encode('utf8');
    user.rank = jsoninfo.Getvalue('rank');
    user.avatar = jsoninfo.Getvalue('face');
    user.follow = jsoninfo.Getvalue('attention');
    user.fans = jsoninfo.Getvalue('fans');
    user.article = jsoninfo.Getvalue('article');
    user.place = jsoninfo.Getvalue('place');
    user.description = jsoninfo.Getvalue('description');
    user.followlist = [];
    for fo in jsoninfo.Getvalue('attentions'):
        user.followlist.append(fo)
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
    jsoninfo = JsonInfo(url);
    vediolist = [];
    for vedio_idx in jsoninfo.Getvalue('list'):
        vedio = Vedio(vedio_idx['aid'],vedio_idx['title']);
        vedio.cover = vedio_idx['cover'];
        vedio.guankan = vedio_idx['click'];
        vediolist.append(vedio);
    return vediolist

def GetComment(aid,page = None,pagesize = None,ver=None,order = None):
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
    url = 'http://api.bilibili.cn/feedback?aid='+GetString(aid);
    if page:
        url += '&page='+GetString(page)
    if pagesize:
        url += '&pagesize='+GetString(pagesize)
    if ver:
        url += '&ver='+GetString(ver)
    if order:
        url += '&order='+GetString(order)
    jsoninfo = JsonInfo(url);
    commentList = CommentList();
    commentList.comments = [];
    commentList.commentLen = jsoninfo.Getvalue('totalResult')
    commentList.page = jsoninfo.Getvalue('pages');
    idx = 0;
    while jsoninfo.Getvalue(str(idx)):
        liuyan = Comment();
        liuyan.lv = jsoninfo.Getvalue(str(idx),'lv')
        liuyan.fbid = jsoninfo.Getvalue(str(idx),'fbid')
        liuyan.msg = jsoninfo.Getvalue(str(idx),'msg')
        liuyan.ad_check = jsoninfo.Getvalue(str(idx),'ad_check')
        liuyan.post_user.mid = jsoninfo.Getvalue(str(idx),'mid');
        liuyan.post_user.avatar = jsoninfo.Getvalue(str(idx),'face');
        liuyan.post_user.rank = jsoninfo.Getvalue(str(idx),'rank')
        liuyan.post_user.name = jsoninfo.Getvalue(str(idx),'nick')
        commentList.comments.append(liuyan);
        idx += 1;
    return commentList

def GetAllComment(aid,ver=None,order = None):
    """
获取一个视频全部评论，有可能需要多次爬取，所以会有较大耗时
输入：
    aid：AV号
    ver：API版本,最新是3
    order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序
返回：
    评论列表
    """
    MaxPageSize = 300;
    commentList = GetComment(aid=aid,pagesize=MaxPageSize,ver=ver,order=order)
    if commentList.page == 1:
        return commentList;
    for p in range(2,commentList.page+1):
        #print '%d/%d'%(p*MaxPageSize,commentList.commentLen)
        t_commentlist = GetComment(aid=aid,pagesize=MaxPageSize,page=p,ver=ver,order=order)
        for liuyan in t_commentlist.comments:
            commentList.comments.append(liuyan)
        time.sleep(0.5)
    return commentList

def GetVedioInfo(aid,appkey,page = 1,AppSecret=None,fav = None):
    paras = {'id': GetString(aid),'page': GetString(page)};
    if fav != None:
        paras['fav'] = fav;
    url =  'http://api.bilibili.cn/view?'+GetSign(paras,appkey,AppSecret);
    jsoninfo = JsonInfo(url);
    vedio = Vedio(aid,jsoninfo.Getvalue('title'));
    vedio.guankan = jsoninfo.Getvalue('play')
    vedio.commentNumber = jsoninfo.Getvalue('review')
    vedio.danmu = jsoninfo.Getvalue('video_review')
    vedio.shoucang = jsoninfo.Getvalue('favorites');
    vedio.description = jsoninfo.Getvalue('description')
    vedio.tag = [];
    taglist = jsoninfo.Getvalue('tag');
    if taglist != None:
        for tag in taglist.split(','):
            vedio.tag.append(tag);
    vedio.cover = jsoninfo.Getvalue('pic');
    vedio.author = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('author'));
    vedio.page = jsoninfo.Getvalue('pages');
    vedio.date = jsoninfo.Getvalue('created_at');
    vedio.credit = jsoninfo.Getvalue('credit');
    vedio.coin = jsoninfo.Getvalue('coins');
    vedio.spid = jsoninfo.Getvalue('spid');
    vedio.cid = jsoninfo.Getvalue('cid');
    vedio.offsite = jsoninfo.Getvalue('offsite');
    vedio.partname = jsoninfo.Getvalue('partname');
    vedio.src = jsoninfo.Getvalue('src');
    vedio.tid = jsoninfo.Getvalue('tid')
    vedio.typename = jsoninfo.Getvalue('typename')
    vedio.instant_server = jsoninfo.Getvalue('instant_server');
    return vedio
    
def GetSign(params,appkey,AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
待添加：【重要！】
    需要做URL编码并保证字母都是大写，如 %2F
    """
    params['appkey']=appkey;
    data = "";
    paras = params.keys();
    paras.sort();
    for para in paras:
        if data != "":
            data += "&";
        data += para + "=" + params[para];
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update(data+AppSecret)
    return data+'&sign='+m.hexdigest()

def GetGangumi(appkey,btype = None,weekday = None,AppSecret=None):
    """
获取新番信息
输入：
    btype：番剧类型 2: 二次元新番 3: 三次元新番 默认：所有
    weekday:周一:1 周二:2 ...周六:6 
    """
    paras = {};
    if btype != None and btype in [2,3]:
        paras['btype'] = GetString(btype)
    if weekday != None:
        paras['weekday'] = GetString(weekday)
    url =  'http://api.bilibili.cn/bangumi?' + GetSign(paras,appkey,AppSecret);
    jsoninfo = JsonInfo(url);
    bangumilist = [];
    for bgm in jsoninfo.Getvalue('list'):
        bangumi = Bangumi();
        bangumi = Bangumi();
        bangumi.typeid = bgm['typeid']
        bangumi.lastupdate = bgm['lastupdate']
        bangumi.areaid = bgm['areaid']
        bangumi.bgmcount = bgm['bgmcount']
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
        bangumilist.append(bangumi)
    return bangumilist
        
#def GetBangumiByTime(year,month):
#    url='http://www.bilibili.tv/index/bangumi/%s-%s.json'%(GetString(year),GetString(month));     
#    print url    
#    jsoninfo = getURLContent(url);
#    print jsoninfo

def GetRank(appkey,tid,begin=None,end=None,page = None,pagesize=None,click_detail =None,order = None,AppSecret=None):
    paras = {};
    paras['appkey']=appkey;
    paras['tid']=GetString(tid);
    if order:
        paras['order']=order;
    if click_detail:
        paras['click_detail']=click_detail;
    if pagesize:
        paras['pagesize']=GetString(pagesize);
    if begin != None and len(begin)==3:
        paras['begin']='%d-%d-%d'%(begin[0],begin[1],begin[2]);
    if end != None and len(end)==3:
        paras['end']='%d-%d-%d'%(end[0],end[1],end[2]);
    if page:
        paras['page']=GetString(page);
    if click_detail:
        paras['click_detail'] = click_detail;
    url = 'http://api.bilibili.cn/list?' + GetSign(paras,appkey,AppSecret);    
    jsoninfo = JsonInfo(url);
    vediolist = [];
    page = jsoninfo.Getvalue('pages')
    name = jsoninfo.Getvalue('name')
    for i in range(len(jsoninfo.Getvalue('list'))-1):
        idx = str(i);
        vedio = Vedio(jsoninfo.Getvalue('list',idx,'aid'),jsoninfo.Getvalue('list',idx,'title'));
        vedio.Iscopy = jsoninfo.Getvalue('list',idx,'copyright')
        vedio.tid = jsoninfo.Getvalue('list',idx,'typeid')
        vedio.typename = jsoninfo.Getvalue('list',idx,'typename')
        vedio.subtitle = jsoninfo.Getvalue('list',idx,'subtitle'); 
        vedio.guankan = jsoninfo.Getvalue('list',idx,'play'); 
        vedio.commentNumber = jsoninfo.Getvalue('list',idx,'review');
        vedio.danmu = jsoninfo.Getvalue('list',idx,'video_review');
        vedio.shoucang = jsoninfo.Getvalue('list',idx,'favorites');
        vedio.author = User(jsoninfo.Getvalue('list',idx,'mid'),jsoninfo.Getvalue('list',idx,'author'))
        vedio.description = jsoninfo.Getvalue('list',idx,'description');
        vedio.date = jsoninfo.Getvalue('list',idx,'create');
        vedio.cover = jsoninfo.Getvalue('list',idx,'pic');
        vedio.credit = jsoninfo.Getvalue('list',idx,'credit');
        vedio.coin = jsoninfo.Getvalue('list',idx,'coins');
        vedio.duration = jsoninfo.Getvalue('list',idx,'duration');
        if click_detail != None:
            vedio.play_site = jsoninfo.Getvalue('list',idx,'play_site');
            vedio.play_forward = jsoninfo.Getvalue('list',idx,'play_forward');
            vedio.play_mobile = jsoninfo.Getvalue('list',idx,'play_mobile');
        vediolist.append(vedio)
    return [page,name,vediolist]
        
        
if __name__ == "__main__":
#    f = open('result.txt','w');
     #获取最热视频
    vedioList = GetPopularVedio([2014,05,20],[2014,05,27],TYPE_BOFANG,0,1)
    for vedio in vedioList:
        print vedio.title
#        vedio.saveToFile(f);
     #获取用户信息
#     user = GetUserInfoBymid('72960');
#     print user.name
#     user = GetUserInfoByName('vespa')
#     print user.spaceName
#    user.saveToFile(f);    
    #获取专题视频信息
#    vediolist = GetVedioOfZhuanti('6492',bangumi=0)
#    for vedio in vediolist:
#        print vedio.title
    #获取评论
#    commentList = GetAllComment('1154794');
#    for liuyan in commentList.comments:
#        print liuyan.lv,'-',liuyan.post_user.name,':',liuyan.msg
#    f.close();
    #获取视频信息
#    appkey='03fc8eb101b091fb';
#    secretkey = None #选填
#    vedio = GetVedioInfo(1152959,appkey=appkey,AppSecret=secretkey);
#    for tag in vedio.tag:
#        print tag
    #获取新番
#    bangumilist = GetGangumi(appkey,btype = 2,weekday=1,AppSecret=secretkey);
#    for bangumi in bangumilist:
#        print bangumi.scover,bangumi.mcover,bangumi.cover
    #获取分类排行
#    [page,name,vediolist] = GetRank(appkey,tid='0',order='hot',page=12,pagesize = 100,begin=[2014,1,1],end=[2014,2,1],click_detail='true')  
#    for vedio in vediolist:
#        print vedio.title,vedio.play_site