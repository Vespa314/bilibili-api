# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""


from support import * 
import hashlib
import datetime
import sys





import xml.etree.ElementTree as et
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Feedback():
    """Feeback used by Alfred Script Filter

    Usage:
        fb = Feedback()
        fb.add_item('Hello', 'World')
        fb.add_item('Foo', 'Bar')
        print fb

    """

    def __init__(self):
        self.feedback = et.Element('items')

    def __repr__(self):
        """XML representation used by Alfred

        Returns:
            XML string
        """
        return et.tostring(self.feedback)

    def add_item(self, title, subtitle = "", arg = "", valid = "yes", autocomplete = "", icon = "icon.png"):
        """
        Add item to alfred Feedback

        Args:
            title(str): the title displayed by Alfred
        Keyword Args:
            subtitle(str):    the subtitle displayed by Alfred
            arg(str):         the value returned by alfred when item is selected
            valid(str):       whether or not the entry can be selected in Alfred to trigger an action
            autcomplete(str): the text to be inserted if an invalid item is selected. This is only used if 'valid' is 'no'
            icon(str):        filename of icon that Alfred will display
        """
        item = et.SubElement(self.feedback, 'item', uid=str(len(self.feedback)), arg=arg, valid=valid, autocomplete=autocomplete)
        _title = et.SubElement(item, 'title')
        _title.text = title
        _sub = et.SubElement(item, 'subtitle')
        _sub.text = subtitle
        _icon = et.SubElement(item, 'icon')
        _icon.text = icon



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
    for i in range(len(jsoninfo.Getvalue('list'))-1):
        idx = str(i);
        item = jsoninfo.Getvalue('list',idx);
        vedio = Vedio(item['aid'],item['title']);
        vedio.guankan = item['play']; 
        vedio.tid = item['typeid']; 
        vedio.author = User(item['mid'],item['author'])
        vedio.description = item['description'];
        vedio.duration = item['duration'];
        vediolist.append(vedio)
    return vediolist
        
query = '{query}'
fb = Feedback()
appkey = "03fc8eb101b091fb"
dayspan = 3

modelist = {'dm':'damku','sc':'stow','pl':"review",'yb':'promote'}
mode = None
for k in modelist:
    opt = re.findall(k,query)
    if opt != []:
        mode = modelist[k]
        break
if mode == None:
    mode = 'hot'

zonelist = {'dh':1,'yy':3,'yx':4,'kj':36,'yl':5}
zone = None
for k in zonelist:
    opt = re.findall(k,query)
    if opt != []:
        zone = zonelist[k]
        break
if zone == None:
    zone = 0
    
opt = re.findall(r'd(\d+)',query)
if opt != []:
    dayspan = int(opt[0])
    if dayspan > 90:
        dayspan = 3


endday = datetime.datetime.now()
beginday = endday - datetime.timedelta(days =dayspan)
            
vediolist = GetRank(appkey,zone,begin=[beginday.year,beginday.month,beginday.day],end=[endday.year,endday.month,endday.day],page = None,pagesize=30,click_detail =None,order = mode,AppSecret=None)

try:
    for bgm in vediolist:
        if bgm.tid not in [33,32,94]:
            fb.add_item("%s(%s)"%(bgm.title,str(bgm.guankan)),subtitle="【%s】%s"%(bgm.author.name,bgm.description),arg=bgm.aid)
    
except SyntaxError as e:
    if ('EOF', 'EOL' in e.msg):
        fb.add_item('...')
    else:
        fb.add_item('SyntaxError', e.msg)
except Exception as e:
        fb.add_item(e.__class__.__name__,subtitle=e.message)    
print fb
