#coding=utf-8

import sys
import gzip
import json
import hashlib
import re
import urllib2
import xml.dom.minidom
import zlib

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'
APPKEY = '85eb6835b0a1034e'
APPSEC = '2ad42749773c441109bdc0191257a664'

def GetBilibiliUrl(url):
    overseas=False
    url_get_media = 'http://interface.bilibili.com/playurl?' if not overseas else 'http://interface.bilibili.com/v_cdn_play?'
    regex_match = re.findall('http:/*[^/]+/video/av(\\d+)(/|/index.html|/index_(\\d+).html)?(\\?|#|$)',url)
    if not regex_match:
        raise ValueError('Invalid URL: %s' % url)
    aid = regex_match[0][0]
    pid = regex_match[0][2] or '1'
    cid_args = {'type': 'json', 'id': aid, 'page': pid}
    resp_cid = urlfetch('http://api.bilibili.com/view?'+GetSign(cid_args,APPKEY,APPSEC))
    resp_cid = dict(json.loads(resp_cid.decode('utf-8', 'replace')))
    cid = resp_cid.get('cid')
    media_args = {'otype': 'json', 'cid': cid, 'type': 'mp4', 'quality': 4, 'appkey': APPKEY}
    resp_media = urlfetch(url_get_media+GetSign(media_args,APPKEY,APPSEC))
    resp_media = dict(json.loads(resp_media.decode('utf-8', 'replace')))
    res = []
    for media_url in resp_media.get('durl'):
        res.append(media_url.get('url'))
    return res

def GetSign(params,appkey,AppSecret=None):
    params['appkey']=appkey
    data = ""
    paras = sorted(params)
    paras.sort()
    for para in paras:
        if data != "":
            data += "&"
        data += para + "=" + str(params[para])
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update((data+AppSecret).encode('utf-8'))
    return data+'&sign='+m.hexdigest()

def urlfetch(url):
    req_headers = {'User-Agent': USER_AGENT}
    req = urllib2.Request(url=url, headers=req_headers)
    return urllib2.urlopen(req).read()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('输入视频播放地址')
    else:
        media_urls = GetBilibiliUrl(sys.argv[1])
        for media_url in media_urls:
            print media_url
