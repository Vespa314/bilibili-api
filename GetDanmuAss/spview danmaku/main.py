# -*- coding: utf-8 -*-
"""
@author: Vespa
"""

import sys
import os
from bilibili import *
from GetAssDanmaku import *
def main(argv):
    appkey = '70472776da900153'
    secretkey = 'f7d9146f9363f3407d31098918493336'
    SPList = biliZhuantiSearch(appkey,secretkey,argv)
    if 0 == len(SPList):
        print "【Error】SPview Not Found!!"
        return
    for idx,sp in enumerate(SPList):
        print "[%d]:%s(spid = %d)"%(idx+1,sp.title,getint(sp.spid))
    choise = int(raw_input("请选择专题:"))-1

    if choise < 0 or choise >= len(SPList):
        print "【Error】Range Error"
        return
    else:
        print "\n"

    print "【Info】Getting Video info of %s"%(SPList[choise].title)
    videoList = GetVideoOfZhuanti(SPList[choise].spid,SPList[choise].season_id,1)
    if len(videoList) == 0:
        print "【Error】Vedio Not Found!!"
        return

    # fid = open('%s.rule'%(SPList[choise].title),'w')
    # for video in videoList:
    #     url= "http://www.bilibili.com/video/av%d/"%(video.aid)
    #     # print video.title
    #     for mediaurl in GetBilibiliUrl(url,appkey,secretkey):
    #         print mediaurl
    #         filename = GetRE(mediaurl,'[^\.|/]+\.(flv|hlv)')
    #         fid.write('%s->%s'%(filename[0],video.title))
    # fid.close()
    # 视频合并待实现

    for video in videoList:
        Danmaku2ASS(GetDanmuku(video.cid),r'%s/Desktop/%s.ass'%(os.path.expanduser('~'),video.title.replace(r'/','')), 640, 360, 0, 'sans-serif', 15, 0.5, 10, False)
        print "%s Download Finished!"%(video.title)
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "【Error】python main.py xxx"
    else:
        main(sys.argv[1])