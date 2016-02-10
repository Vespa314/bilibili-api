#coding=utf-8

import requests
import time

def post_heartbeat(headers):
    url = 'http://live.bilibili.com/User/userOnlineHeart'
    response = requests.post(url, headers=headers)
    print response.content

def read_cookie(cookiepath):
    with open(cookiepath, 'r') as fid:
        cookies = fid.readlines()
    return cookies

def main(headers = {}):
    while True:
        print "Post:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        post_heartbeat(headers)
        time.sleep(300)

if __name__=='__main__':
    cookies = read_cookie('./bilicookies')[0]
    headers = {
        'accept-encoding': 'gzip, deflate, sdch',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.16 Safari/537.36',
        'authority': 'live.bilibili.com',
        'cookie': cookies,
        # 'Referer':'http://live.bilibili.com/39936',
    }
    main(headers)