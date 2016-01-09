# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 00:00:22 2014

@author: Administrator
"""
from bilibili import *
import os
import zipfile

def videowrite(f,video):
    if video.title:
        f.write('Aid:%s\nTitle:%s\n'%(video.aid,video.title))
    else:
        f.write('Aid:%s\nTitle:NULL\n'%(video.aid))
    f.write('copyright:%s\n'%(video.Iscopy))
    f.write('Click:%s\nDanmu:%s\n'%(video.guankan,video.danmu))
    f.write('comment:%s\n'%(video.commentNumber))
    f.write('credit:%s\n'%(video.credit))
    f.write('coin:%s\n'%(video.coin))
    f.write('favorite:%s\n'%(video.shoucang))
    if video.author.name:
        f.write('author:%s %s\n'%(video.author.name,video.author.mid))
    else:
        f.write('author:%s %s\n'%('NULL',video.author.mid))
    f.write('date:%s\n'%(video.date))
    f.write('duration:%s\n'%(video.duration))
    f.write('play_site:%s\n'%(video.play_site))
    f.write('play_forward:%s\n'%(video.play_forward))
    f.write('play_mobile:%s\n'%(video.play_mobile))
    f.write('description:%s\n'%(video.description))
    f.write('pic:%s\n'%(video.cover))
    f.write('\n')

def linecount_2(filename):
    count = -1 #让空文件的行号显示0
    for count,line in enumerate(open(filename,'r')):
        pass
    return count+1

def GetAllVideo(year,month):
    appkey = '*******'
    begin = [year,month,1]
    end = [year,month,31]

    path = '/root/tmp/bilibili/%d-%d/'%(year,month)
    print '%d-%d'%(year,month)
    if not os.path.exists(path):
        os.mkdir(path)

    fid_dict = {}
    tid_set = set([])

    illegalSymble = list('/:?|<>*')

    for page in xrange(1,9999999):
        total_page = -1
        stay_time = 5
        while total_page == -1:
            [total_page,_name,videolist] = GetRank(appkey,tid=0,order='hot',pagesize = 100,page=page,begin=begin,end=end,click_detail='true')
            if total_page == -1:
                time.sleep(stay_time)
                stay_time += 5
        print '\t%s:page %d/%d'%(time.strftime('%H:%M:%S',time.localtime(time.time())),page,total_page)
        for video in videolist:
            if not video.tid in tid_set:
                for sym in illegalSymble:
                    video.typename = video.typename.replace(sym,'')
                fid_dict[video.tid] = open('%s%d-%s.txt'%(path,video.tid,video.typename),'w')
                tid_set.add(video.tid)
            videowrite(fid_dict[video.tid],video)

        if page == total_page:
            break
        time.sleep(3)
    for fid in fid_dict:
        fid_dict[fid].close()
    z = zipfile.ZipFile('/root/Dropbox/bili_video/video/%s.zip'%('%d-%d'%(year,month)), 'w')
    for d in os.listdir(path):
        z.write(path+os.sep+d)
    z.close()
    __import__('shutil').rmtree(path)

if __name__ == "__main__":
    for year in range(2009,2017):
        for month in range(1,13):
            if year == 2016 and month >= 1:
                continue;
            if year == 2009 and month < 6:
                continue
            if os.path.isfile('/root/Dropbox/bili_video/video/%s.zip'%('%d-%d'%(year,month))):
                print year,'/',month," existed"
                continue
            GetAllVideo(year,month)
    print 'finished'
