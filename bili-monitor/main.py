# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""

from bilibili import *
import os

def fileRename(title):
    if title.find('/') >= 0:
        title = title.replace('/','');
    if title.find(':') >= 0:
        title = title.replace(':','');
    if title.find('?') >= 0:
        title = title.replace('?','');
    if title.find('|') >= 0:
        title = title.replace('|','');
    if title.find('<') >= 0:
        title = title.replace('<','');
    if title.find('>') >= 0:
        title = title.replace('>','');
    if title.find('*') >= 0:
        title = title.replace('*','');
    return title

def mMkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

if __name__ == "__main__":
    appkey='03fc8eb101b091fb';
    secretkey = None #选填
    bangumilist = GetBangumi(appkey,btype = 2,weekday=0,AppSecret=secretkey);
    for bangumi in bangumilist:
        bangumi.title = fileRename(bangumi.title)
        print "updating bangumi info of:",bangumi.title
        path = "./%s"%(bangumi.title)
        mMkdir(path)
        videolist = GetVideoOfZhuanti(str(bangumi.spid),bangumi=1,season_id=bangumi.season_id)
        for video in videolist:
            print "Getting info of:",video.title
            videoinfo = GetVideoInfo(video.aid,appkey=appkey,AppSecret=secretkey)
            filepath = "%s/%s.txt"%(path,video.episode)
            if not os.path.isfile(filepath):
                fid = open(filepath,"a+")
                bgminfo = "Name:%s\nav=%s\nfrom:%s\nupdate day:%s\n"%(videoinfo.title,videoinfo.aid,video.src,videoinfo.date)
                fid.write(bgminfo)
            else:
                fid = open(filepath,"a+");
            cur_time = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))

            info = "%s: gk(%s) pl(%s) dm(%s) sc(%s) yb(%s)\n"%(cur_time,videoinfo.guankan,videoinfo.commentNumber,videoinfo.danmu,videoinfo.shoucang,videoinfo.coin)
            fid.write(info)
            fid.close()
            time.sleep(1)