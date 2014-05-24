##直接爬取视频排行:
* 获取URL: `http://www.bilibili.tv/list/[stow]-[zone]-[page]-[year1]-[month1]-[day1]~[year2]-[month2]-[day2].html`

* 返回：只关于视频部分的源码

* 提取正则表达式：XXXXXXX【待补充】

###参数说明：

####Type:排序方式
* **收藏**：stow
* **评论数**：review
* **播放数**：hot
* **硬币数**：promote
* **用户评分**：comment
* **弹幕数**：damku
* *拼音*：pinyin-{x}，x可以是A~Z中的一个
* *投稿时间*：default

>**注意：**上面排序方式中，**粗体字(前六个)**部分可以获取下文描述一切分区，但是*斜体(后两个)*只能获取二级以后的分区，也就是说**不可以**通过`拼音`和`投稿时间`来获取`综合排名`,`动画`,`音乐/舞蹈`,`游戏`,`科学技术`,`娱乐`,`影视`,`动画剧番`等分区。【可能是可以的，但是我没找到方法:-D】

####zone：分区
* **综合排名**：0
* **动画**：1
    * AMD·AMV：24
    * MMD·3D：25
    * 原创·配音：47
        * 原创：48
        * 中配：49
    * 二次元鬼畜：26
    * 综合：27
        * 手书：50
        * 咨询：51
        * 杂谈：52
        * 其他：53
* **音乐/舞蹈**：3
    * 音乐视频：28
        * OP/ED：54
        * 其他：55
    * Vocaloid相关：30
        * Vocaloid：56
        * UTAU相关：57
        * 中文曲：58
    * 翻唱：31
    * 舞蹈：20
    * 演奏：59
    * 三次元音乐：29
* **游戏**：4
    * 游戏视频：17
        * 预告·演示：61
        * 其他：63
    * 游戏攻略·解说：18
        * 单机游戏：64
        * 网络游戏：65
        * 家用·掌机：66
        * 其他：67
    * Mugen：19
    * 电子竞技：60
        * 赛事：68
        * 解说：69
        * 其它：70
* **科学技术**:36
    * 全球科技：39
        * 数码科技：95
        * 军事科技：96
        * 手机测评：97
        * 其它：98
    * 科普·人文：37
        * BBC纪录片：99
        * 探索频道：100
        * 国家地理：101
        * NHK：102
        * TED演讲：103
        * 名校公开课：104
        * 教程·演示：105
        * 其它：107
    * 野生技术协会：40
    * 趣味短片·其它：108
* **娱乐**：5
    * 生活娱乐：21
    * 三次元鬼畜：22
    * 动物圈：75
        * 喵星人：77
        * 汪星人：78
        * 其它：79
    * 美食：76
        * 美食视频：80
        * 制作教程：81
    * 综艺：71
* **影视**：11
    * 连载剧集：15
        * 国产：110
        * 日剧：111
        * 美剧：112
        * 其它：113
    * 完结剧集：34
        * 国产：87
        * 日剧：88
        * 美剧：89
        * 其它：90
    * 电影：23
        * 预告·花絮：82
        * 电影：83
    * 微电影：85
    * 特摄·布袋：86
        * 特摄：91
        * 布袋戏：92
* **动漫剧番**：13
    * 连载动画：33
    * 完结动画：32
    * 剧场·OVA：94

####page：页数，从1开始

>如果只想查看原创，只需在后面加上`-original`即可，也就是URL=
`http://www.bilibili.tv/list/[stow]-[zone]-[page]-[year1]-[month1]-[day1]~[year2]-[month2]-[day2]-original.html`

---

##新番Index
* 获取URL: `http://www.bilibili.tv/list/b-[firstlatter]-[zone]-[time]-[catalog]-[state]-[style]-[updatetime]-[sorttype]-[weekday]--[page].html`

* 返回：整个网页源代码

* 提取正则表达式：XXXXXXX【待补充】

###参数说明：
http://www.bilibili.tv/list/b--a--t----d---1.html
#### zone:地区
* 不限：a
* 中国大陆：a1
* 日本：a2
* 美国：a3
* 英国：a4
* 加拿大：a5
* 中国香港：a6
* 中国台湾：a7
* 韩国：a8
* 法国：a9
* 德国：a15
* 其它：a16

#### time:上映时间
* 不限：留空即可【前后横杠要保留】
* 范围：1956-2014【有个别日期无法选择。。】

#### state:状态
* 不限：留空即可【前后横杠要保留】
* 连载中：0
* 完结：1

#### firstlatter:首字母
* 不限：留空即可【前后横杠要保留】
* A-Z：A-Z

#### weekday:星期
* 不限：留空即可【前后横杠要保留】
* 周日：0
* 周一到周六：分别取1~n

#### style:影片风格
* 不限：留空即可【前后横杠要保留】
* >1:萝莉  2:御姐 3:正太 4:后宫
5:百合  6:耽美  7:搞笑  8:恋爱
9:机战  10:热血  11:美少女  12:神魔
13:童话  14:教育  15:推理  16:惊悚
17:动作  18:励志  19:神话  20:治愈
21:致郁  22:男性向  23:女性向  24:校园
25:魔法  26:奇幻  27:魔幻  28:科幻
29:日常  30:泡面  31:冒险  32:竞技
33:运动  34:怪物  35:成人  36:真人
37:英雄  38:益智  39:生活  40:宠物
41:都市  42:假想科学  43:战斗
* 可以同时选择多种风格，用逗号隔开即可，如`1,2,4`,不过大部分不存在，要精确的话，可以选择先选择一种，然后根据返回源码即可得知当前风格加上什么风格可以有有效电影存在。

#### updatetime：更新时间
* 不限：留空即可【前后横杠要保留】
* 三天内：0
* 七天内：1
* 半月内：2
* 一月内：3

#### sorttype:排序方式
* 人气排序：a
* 更新排序：d
* 发布时间：n
* 播出日期：p

#### catalog：分类索引
* 全部：t
* 其它：t0
* TV：t1
* OVA&OAD：t2
* 剧场版：t3
* 连续剧：t5
* 电影：t6
* 微电影：t7
>很多没被分类的视频都无法在特定的索引分类下%>_<%

#### page：页数
必填，1~n



---

##B站API(无需认证或登录即可爬取的部分)：
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
