##直接爬取

**收藏数:**
URL:
`http://www.bilibili.tv/list/[stow]-[zone]-[page]-[year1]-[month1]-[day1]~[year2]-[month2]-[day2].html`

Type:排序方式
* 收藏：stow
* 评论数：review
* 播放数：hot
* 硬币数：promote
* 用户评分：comment
* 弹幕数：damku

zone：分区
* 动画：1
* 音乐/舞蹈：3
* 游戏：4
* 娱乐：5
* 影视：11
* 动漫剧番：13
* 科学技术:36
*更多的有待研究*

如果只想查看原创：
`http://www.bilibili.tv/list/[stow]-[zone]-[page]-[year1]-[month1]-[day1]~[year2]-[month2]-[day2]-original.html`

---

##B站API：
**获取本周排行**
* URL：【返回json】
    * `http://api.bilibili.cn/index`
* 返回格式：
    * 第一层为type1，type3，type4，type5，type11，type13，type36，分别代表分区
    * 第二层为0~7表示第1到8名
    * 第三层为详细信息，包括：
        *  aid：AV号
        *  copyright：Original=原创，copy=转载
        *  typeid:更细致分区
        *  typename：类型名
        *  title：标题
        *  subtitle：副标题，很多视频没有
        *  play：播放数
        *  review：评论，少于浏览器看到的，包含回复
        *  video_review：弹幕数【估计包含被清过的】
        *  favorites：收藏
        *  mid：发布者账号
        *  author：发布者
        *  description：描述
        *  create：发布时间
        *  pic：封面
        *  credit：积分
        *  coins：硬币
        *  duration：时长
* 示例：
```
json['type1'][0]['title']
```

**读取作者推荐视频信息**
* URL：【返回json】
    * `http://api.bilibili.cn/author_recommend?aid=[id]`
* 输入：
    * aid：视频AV号 
* 返回格式：
    *  第一层：list
    *  第二层：0~n-1表示推荐的n部视频
    *  第三层：
        *  aid:av号
        *  title：标题
        *  cover：封面
        *  click：播放数
        *  review：评论，少于浏览器看到的，包含回复
        *  favorites：收藏
        *  video_review：弹幕数
* 示例
```
json['list']['0']['title']
```

**读取评论**
* URL：【返回json】
    * `http://api.bilibili.cn/feedback`
* 输入：
    * aid：视频AV号
    * page：页码【选填】
    * pagesize：单页返回的记录条数，最大不超过300，默认为10。【选填】
    * ver：API版本,最新是3【选填】
    * order：排序方式 默认按发布时间倒序 可选：good 按点赞人数排序 hot 按热门回复排序【选填】

* 返回格式：
    *  第一层：
        *  totalResult：总评论数
        *  pages：页数
        *  0~n：评论条数[只有一页的]
    *  第二层(相对于评论条数)：
        *  mid:会员ID
        *  lv：楼层
        *  fbid：评论ID
        *  msg：评论信息
        *  ad_check：状态 (0: 正常 1: UP主隐藏 2: 管理员删除 3: 因举报删除)
        *  face：发布人头像
        *  rank：发布人显示标识
        *  uname：发布人暱称
* 示例
```python
for i in range(0,len(json)-2):
    print JsonInfo[str(i)]['lv'],':',JsonInfo[str(i)]['msg'].encode('gbk','ignore')
```

**读取专题信息**
* URL：【返回json】
    * `http://api.bilibili.tv/sp`
* 输入：
    * spid：专题编号【二选一】
    * title：专题名称【二选一】
* 返回格式：
    * spid：专题SPID
    * title：专题名
    * pubdate：发布日期 (UNIX Timestamp)
    * create_at：发布日期
    * lastupdate：最后更新日期 (UNIX Timestamp)
    * lastupdate_at：最后更新日期
    * alias：同义词
    * cover：封面
    * isbangumi：是否为新番 1=2次元新番 2=3次元新番
    * isbangumi_end：是否已经播放结束
    * bangumi_date：开播日期
    * description：专题简介
    * view：点击次数
    * favourite：专题收藏次数
    * attention：专题被关注次数
    * count：专题视频数量
* 示例
```python
http://api.bilibili.tv/sp?title=VOCALOID
```

**读取专题视频信息**
* URL：【返回json】
    * `http://api.bilibili.tv/sp`
* 输入：
    * spid：专题SPID
    * season_id：专题分季ID【选填】
    * bangumi：设置为1时只返回番剧类视频 设置为0时只返回普通视频 不设置则返回所有视频【选填】
* 返回格式：
    * 第一层：
        * count：视频数目
        * result：返回的记录总数目
        * list：包含视频信息
    * 第二层(相对于list)：
        * 编号 0~result-1表示第1~result个视频
    * 第三层(相对于编号) :
        * aid：AV号
        * cover：封面
        * title：标题
        * click：点击数
        * page：不明，全是0

>说明：关于SPID的获取，暂时只知道`chrome`点击`F12`，然后查看`Network`中html的文件名编号

**读取用户信息**
* URL：【返回json】
    * `http://api.bilibili.cn/userinfo`
* 输入：
    * user：昵称【二选一】
    * mid：用户ID【二选一】
* 返回格式：
    * mid：会员ID
    * name：暱名
    * approve：是否为认证帐号
    * spacename：空间名
    * sex：性别 (男/女/不明)
    * rank：帐号显示标识
    * face：小头像
    * attention：关注的好友人数
    * fans：粉丝人数
    * article：投稿数
    * place：所在地
    * description：认证用户为认证信息 普通用户为交友宣言
    * attentions：关注的好友列表


