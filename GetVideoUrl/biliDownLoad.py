#!/usr/bin/env python3
#Modified by SuperFashi

import sys
import gzip
import json
import hashlib
import re
import urllib.parse
import urllib.request
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
    media_urls = resp_media.get('durl')
    media_urls = media_urls[0]
    media_urls = media_urls.get('url')
    return media_urls

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
    req_headers = {'Accept-Encoding': 'gzip, deflate', 'User-Agent': USER_AGENT}
    req = urllib.request.Request(url=url, headers=req_headers)
    response = urllib.request.urlopen(req, timeout=120)
    content_encoding = response.info().get('Content-Encoding')
    if content_encoding == 'gzip':
        data = gzip.GzipFile(fileobj=response).read()
    elif content_encoding == 'deflate':
        decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
        data = decompressobj.decompress(response.read())+decompressobj.flush()
    else:
        data = response.read()
    return data

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('输入视频播放地址')
    else:
        media_urls = GetBilibiliUrl(sys.argv[1])
        print(media_urls)
