# -*- coding: utf-8 -*-
"""
Created on Fri Jun 06 18:48:19 2014

@author: Administrator
"""
import re
import os

def changecoder(item):
    try:
        item.decode('utf8')
        k=item
    except:
        k = item.decode('gbk').encode('utf8');
    k = k.replace(",","")
    return k

def FileCheck(year,month,tid):
    filepath = './%d-%d/%d.txt'%(year,month,tid);
    f = open(filepath,'r')
    info = ['']*16;
    for count,line in enumerate(f):
        if count % 17 == 0:
            info[0] = re.findall('Aid:(\d+)',line);
        if count % 17 == 1:
            info[1]  = re.findall('Title:(.+)$',line);
        if count % 17 == 2:    
            info[2]  = re.findall('Typeid:(\d+)',line);
        if count % 17 == 3:    
            info[3]  = re.findall('Typename:(.*)$',line);
        if count % 17 == 4:    
            info[4]  = re.findall('Click:(\d+)',line);
        if count % 17 == 5:    
            info[5]  = re.findall('Danmu:(\d+)',line);
        if count % 17 == 6:    
            info[6]  = re.findall('comment:-?(\d+)',line);
        if count % 17 == 7:    
            info[7]  = re.findall('favorite:(\d+)',line);
        if count % 17 == 8:    
            info[8]  = re.findall('author:(.+) (\d+)$',line);
            if info[8] == []:
                info[8]  = re.findall('author:(.+) (None)$',line);
        if count % 17 == 9:    
            info[9]  = re.findall('date:(\d+)-(\d+)-(\d+) (\d+):(\d+)',line);
        if count % 17 == 10:    
            info[10]  = re.findall('credit:(\d+)',line);
        if count % 17 == 11:    
            info[11]  = re.findall('coin:(\d+)',line);
        if count % 17 == 12:    
            info[12]  = re.findall('duration:(\d+):(\d+)',line);
        if count % 17 == 13:    
            info[13]  = re.findall('play_site:(\d+)',line);
        if count % 17 == 14:    
            info[14]  = re.findall('play_forward:(\d+)',line);
        if count % 17 == 15:    
            info[15]  = re.findall('play_mobile:(\d+)',line);
            for i in range(16):
                if info[i] == [] and i not in [4,12]:
                    print year,month,tid,i,count+1
    f.close()

def ReCreateFile(year,month,tid):
    global vdict
    filepath = './%d-%d/%d.txt'%(year,month,tid);
    f = open(filepath,'r')
    info = []
    for count,line in enumerate(f):
        if count % 17 == 0:
            t = re.findall('Aid:(\d+)',line)
            info.append(t[0])
        if count % 17 == 1:
            t = re.findall('Title:(.+)$',line)
            info.append(t[0])
        if count % 17 == 2:    
            t = re.findall('Typeid:(\d+)',line)
            info.append(t[0])
        if count % 17 == 3:    
            t = re.findall('Typename:(.*)$',line)
            info.append(t[0])
        if count % 17 == 4:    
            t = re.findall('Click:(.*)$',line)
            info.append(t[0])
        if count % 17 == 5:    
            t = re.findall('Danmu:(\d+)',line)
            info.append(t[0])
        if count % 17 == 6:    
            t = re.findall('comment:(-?\d+)',line)
            info.append(t[0])
        if count % 17 == 7:    
            t = re.findall('favorite:(\d+)',line)
            info.append(t[0])
        if count % 17 == 8:    
            t = re.findall('author:(.*) (\d+)$',line)
            if t == []:
                t = re.findall('author:(.+) (None)$',line)
                info.append([t[0][0],'0'])
            else:
                info.append([t[0][0],t[0][1]])
        if count % 17 == 9:    
            t = re.findall('date:(\d+)-(\d+)-(\d+) (\d+):(\d+)',line)
            info.append([t[0][i] for i in [0,1,2,3,4]])
        if count % 17 == 10:    
            t = re.findall('credit:(\d+)',line)
            info.append(t[0])
        if count % 17 == 11:    
            t = re.findall('coin:(\d+)',line)
            info.append(t[0])
        if count % 17 == 12:    
            t = re.findall('duration:(\d+:\d+)',line)
            if t != []:
                info.append(t[0])
            else:
                info.append('0:0')
        if count % 17 == 13:    
            t = re.findall('play_site:(\d+)',line)
            info.append(t[0])
        if count % 17 == 14:    
            t = re.findall('play_forward:(\d+)',line)
            info.append(t[0])
        if count % 17 == 15:    
            t = re.findall('play_mobile:(\d+)',line)
            info.append(t[0])
    f.close()
    for i in range(len(info)/16):
        aid = int(info[i*16])
        if aid in vdict:
            continue
        else:
            vdict.add(aid);
        y = int(info[i*16+9][0]);
        m = int(info[i*16+9][1]);
        mtid = int(info[i*16+2]);
        if not os.path.exists('./database/%d-%d'%(y,m)):
            os.mkdir('./database/%d-%d'%(y,m))
        path = './database/%d-%d/%d.txt'%(y,m,mtid)
        if not os.path.exists(path):
            f = open(path,'w');
        else:
            f = open(path,'a+');
        for item in range(0,16):
            if item == 9 or item == 8:
                for k in info[i*16+item]:
                    f.write(changecoder(k)+',')
            else:
                f.write(changecoder(info[i*16+item])+',')
        type1 = GetClass1(mtid)
        type2 = GetClass2(mtid)
        if type1 == None or type2 == None:
            print "error",mtid
        f.write('%d,'%type1[0])
        f.write(changecoder(type1[1])+',')
        f.write('%d,'%type2[0])
        f.write(changecoder(type2[1]))
        f.write('\n')
        f.close();            

def linecount(filename):
    count = -1
    for count,line in enumerate(open(filename,'r')):
        pass
    return count+1

def GetClassTree(year,month,tid):
    global vtypedic;
    filepath = './%d-%d/%d.txt'%(year,month,tid);
    f = open(filepath,'r')
    info = []
    for count,line in enumerate(f):
        if count % 17 == 2:    
            t = re.findall('Typeid:(\d+)',line)
            info.append(t[0])
        if count % 17 == 3:    
            t = re.findall('Typename:(.*)$',line)
            info.append(t[0])
    f.close()
    if len(info) == 0:
        return;
    if not vtypedic.has_key(tid):
        vtypedic[tid] = set([]);
    for i in range(len(info)/2):
        k = info[2*i]+','+changecoder(info[2*i+1]);
        k = k.decode('utf8').encode('gbk')
        if k not in vtypedic[tid]:
            vtypedic[tid].add(k)
        
def counteritem(year,month):
    path = './database/%d-%d'%(year,month)
    sum = 0;
    for dirname,subsir,filelists in os.walk(path):
        for filelist in filelists:
            sum += linecount('./database/%d-%d/%s'%(year,month,filelist))
    print '{{%d,%d},%d},'%(year,month,sum),
    
def GetClass2(id):
    if id == 24:
        return [24,"MAD·AMV"]
    elif id in [25,43,44,45,46]:
        return [25,"MMD·3D"]
    elif id in [26]:
        return [26,"二次元鬼畜"]
    elif id in [27,50,51,52,53]:
        return [27,"综合"]
    elif id in [47,48,49]:
        return [47,"原创配音"]
    elif id in [27,50,51,52,53]:
        return [27,"综合"]
    elif id == 20:
        return [20,"舞蹈"]
    elif id in [28,54,55]:
        return [28,"音乐视频"]
    elif id in [30,56,57,58]:
        return [30,"Vocaloid相关"]
    elif id == 29:
        return [29,"三次元音乐"]
    elif id == 31:
        return [31,"翻唱"]
    elif id == 59:
        return [59,"演奏"]
    elif id == 16:
        return [16,"flash游戏"]
    elif id == 19:
        return [19,"Mugen"]
    elif id in [17,61,63]:
        return [17,"游戏视频"]
    elif id in [18,64,65,66,67]:
        return [18,"游戏攻略解说"]
    elif id in [60,68,69,70]:
        return [60,"电子竞技"]
    elif id in [21,71,72,73,74,114,115]:
        return [21,"生活娱乐"]
    elif id in [22]:
        return [22,"三次元鬼畜"]
    elif id in [75,77,78,79]:
        return [75,"动物圈"]
    elif id in [76,80,81]:
        return [76,"美食"]
    elif id in [15,110,111,112,113]:
        return [15,"连续剧"]
    elif id in [34,87,88,89,90]:
        return [34,"完结剧集"]
    elif id in [23,82,83]:
        return [23,"电影"]
    elif id in [85]:
        return [85,"微电影"]
    elif id in [86,91,92]:
        return [86,"特摄布袋"]
    elif id in [12,41]:
        return [12,"公告"]
    elif id in [32]:
        return [32,"连载动画"]
    elif id in [33]:
        return [33,"完结动画"]
    elif id in [94]:
        return [94,"剧场·OVA"]
    elif id in [37,99,100,101,102,103,104,105,107]:
        return [37,"科普人文"]
    elif id in [39,95,96,97,98]:
        return [39,"全球科技"]
    elif id in [108]:
        return [108,"趣味短片·其他"]
    elif id in [40]:
        return [40,"野生技术协会"]
    return None

def GetClass1(id):
    idx = GetClass2(id);
    idx = idx[0]
    if idx in [1,24,25,26,27,47]:
        return [1,"动画"]
    elif idx in [3,20,28,30,29,31,59]:
        return [3,"音乐/舞蹈"]
    elif idx in [4,16,17,18,19,60]:
        return [4,"游戏"]
    elif idx in [5,21,22,75,76]:
        return [5,"娱乐"]
    elif idx in [11,15,34,23,85,86]:
        return [11,"影视"]
    elif idx in [12]:
        return [12,"公告"]
    elif idx in [13,32,33,94]:
        return [13,"剧番"]
    elif idx in [36,37,39,40,108]:
        return [36,"科学技术"]
    return None

#vdict = set([]);
#vtypedic = {};
#for year in range(2009,2015):
#    for month in range(1,13):
#        if year == 2014 and month >= 7:
#            continue
#        if year == 2009 and month <= 5:
#            continue
#        print year,month
#        for tid in range(1,114):
##            GetClassTree(year,month,tid)
#            ReCreateFile(year,month,tid)


#for key in vtypedic:
##    if len( vtypedic[key]) > 1:
##        continue
#    print key
#    ll = list(vtypedic[key]);
#    ll.sort()
#    for item in ll:
#        t = re.findall('(\d+),(.+)$',item);
#        t = t[0]
#        print '\t%s:%s'%(t[0],t[1])
##    print '\n',



tdic = {1:"动画",24:"MAD·AMV",25:"MMD·3D",43:"舞蹈",44:"剧情",45:"原创模型",46:"其他",26:"二次元鬼畜",27:"综合",50:"手书",51:"资讯",52:"杂谈",53:"其他",47:"原创配音",48:"原创动画",49:"中配动画",3:"音乐/舞蹈",20:"舞蹈",28:"音乐视频",54:"OP/ED",55:"其他",30:"Vocaloid相关",56:"Vocaloid",57:"UTAU相关",58:"中文曲",29:"三次元音乐",31:"翻唱",59:"演奏",4:"游戏",16:"flash游戏",17:"游戏视频",61:"预告·演示",63:"其他",19:"Mugen",18:"游戏攻略解说",64:"单机游戏",65:"网络游戏",66:"家用·掌机",67:"其他",60:"电子竞技",68:"赛事",69:"解说",70:"其他",5:"娱乐",21:"生活娱乐",71:"综艺",114:"国内综艺",115:"海外综艺",72:"体育",73:"三次元剪影",74:"其他",22:"三次元鬼畜",75:"动物圈",77:"喵星人",78:"汪星人",79:"其他",76:"美食",80:"美食视频",81:"制作教程",11:"影视",15:"连续剧",110:"国产",111:"日剧",112:"美剧",113:"其他",34:"完结剧集",87:"国产",88:"日剧",89:"美剧",90:"其他",23:"电影",82:"预告·花絮",83:"电影",85:"微电影",86:"特摄布袋",91:"特摄",92:"布袋戏",12:"公告",12:"公告",41:"暂置区",13:"剧番",32:"完结动画",33:"连载动画",94:"剧场·OVA",36:"科学技术",37:"科普人文",99:"BBC纪录片",100:"探索频道",101:"国家地理",102:"NHK",103:"TED演讲",104:"名校公开课",105:"教程·演示",107:"其他",39:"全球科技",95:"数码科技",96:"军事科技",97:"手机评测",98:"其他",108:"趣味短片·其他",40:"野生技术协会"}
for i in tdic:
    print '%d->"%s",'%(i,tdic[i].decode('utf8').encode('gbk')),

"""
1:动画
	24:MAD·AMV
	25:MMD·3D
		43:舞蹈
		44:剧情
		45:原创模型
		46:其他
	26:二次元鬼畜
	27:综合
		50:手书
		51:资讯
		52:杂谈
		53:其他
	47:原创配音
		48:原创动画
		49:中配动画
3：音乐/舞蹈
	20:舞蹈
	28:音乐视频
 	 	54:OP/ED
	 	55:其他
	30:Vocaloid相关
		56:Vocaloid
		57:UTAU相关
		58:中文曲
	29:三次元音乐
	31:翻唱
	59:演奏
4：游戏
	16:flash游戏
	17:游戏视频
		61:预告·演示
		63:其他
	19:Mugen
	18:游戏攻略解说
		64:单机游戏
		65:网络游戏
		66:家用·掌机
		67:其他
	60:电子竞技
		68:赛事
		69:解说
		70:其他
5：娱乐
	21:生活娱乐
		71:综艺
			114:国内综艺
			115:海外综艺
		72:体育
		73:三次元剪影
		74:其他
	22:三次元鬼畜
	75:动物圈
		77:喵星人
		78:汪星人
		79:其他
	76:美食
 		80:美食视频
		81:制作教程
11:影视
	15:连续剧
		110:国产
		111:日剧
		112:美剧
		113:其他
	34：完结剧集
		87:国产
		88:日剧
		89:美剧
		90:其他
	23:电影
		82:预告·花絮
		83:电影
	85:微电影
	86:特摄布袋
		91:特摄
		92:布袋戏
12：公告
	12:公告
	41:暂置区
13:剧番
	32:完结动画
	33:连载动画
	94:剧场·OVA
36:科学技术
	37：科普人文
		99:BBC纪录片
		100:探索频道
		101:国家地理
		102:NHK
		103:TED演讲
		104:名校公开课
		105:教程·演示
		107:其他
	39:全球科技
		95:数码科技
		96:军事科技
		97:手机评测
		98:其他
	108:趣味短片·其他
	40:野生技术协会
"""
print 'finished'



