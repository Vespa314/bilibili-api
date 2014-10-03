# -*- coding: utf-8 -*-

import sys
import re
import zlib
import urllib2

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

query = '{query}'
url = "http://www.bilibili.com/search?keyword=%s&orderby=&formsubmit="%query
req = urllib2.Request(url = url);
content = urllib2.urlopen(req,timeout = 10).read();
content = zlib.decompress(content, 16+zlib.MAX_WBITS)

reg = r'<div class="r"><a href="http://www.bilibili.tv/video/av(\d+)/" target="_blank"><div class="t"><span>([^<]*)</span>([^<]*)</div></a>';
result = re.findall(reg,content,re.S)
fb = Feedback()

try:
    for item in result:
        avnum =  item[0]
        avtype = item[1]
        title = item[2].strip()
        fb.add_item(title,subtitle="%s : http://www.bilibili.tv/video/%s"%(avtype,avnum),arg=avnum)
    
except SyntaxError as e:
    if ('EOF', 'EOL' in e.msg):
        fb.add_item('...')
    else:
        fb.add_item('SyntaxError', e.msg)
except Exception as e:
        fb.add_item(e.__class__.__name__,subtitle=e.message)    
print fb
    