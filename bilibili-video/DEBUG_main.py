# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 00:00:22 2014

@author: Administrator
"""
from bilibili import *
import os

def videowrite(f,video):
    
    f.write('Aid:%s\nTitle:%s\n'%(video.aid.encode('utf8'),video.title.encode('utf8')))
    f.write('copyright:%s\n'%(video.Iscopy.encode('utf8')))
    f.write('Typeid:%s\nTypename:%s\n'%(video.tid,video.typename.encode('utf8')))
    f.write('Click:%s\nDanmu:%s\n'%(video.guankan,video.danmu))
    f.write('comment:%s\n'%(video.commentNumber))
    f.write('favorite:%s\n'%(video.shoucang))
    if video.author.name:
        f.write('author:%s %s\n'%(video.author.name.encode('utf8'),video.author.mid))
    else:
        f.write('author:%s %s\n'%('NULL',video.author.mid))
    f.write('date:%s\n'%(video.date))
    f.write('credit:%s\n'%(video.credit))
    f.write('coin:%s\n'%(video.coin))
    f.write('duration:%s\n'%(video.duration))
    f.write('play_site:%s\n'%(video.play_site))
    f.write('play_forward:%s\n'%(video.play_forward))
    f.write('play_mobile:%s\n'%(video.play_mobile))
    f.write('\n')

def linecount_2(filename):
    count = -1 #让空文件的行号显示0
    for count,line in enumerate(open(filename,'r')):
        pass
    return count+1

def Check(appkey,tid,begin,end,path):
    filepath = './%s/%d.txt'%(path,tid)
    [pages,number,videolist] = GetRank(appkey,tid,order='hot',pagesize = 100,begin=begin,end=end,click_detail='true')
    time.sleep(3)
    linenum = int(linecount_2(filepath)/17);
    print time.strftime('%H:%M:%S',time.localtime(time.time())),
    if number > linenum:
        if abs(number-linenum-len(videolist)) < 5:
            print 'All 100:',begin[0:2],tid,number,linenum,len(videolist)
            f = open('./%s/%d.txt'%(path,tid),'a+');
            for video in videolist:
                videowrite(f,video);
            f.close()
        else:
            print 'lose:',begin[0:2],tid,number,linenum
            GetAllVideo(appkey,tid,begin,end,path)
    elif number < linenum:
        print 'now lost:',begin[0:2],tid,number,linenum
    elif number == linenum:
        print 'match:',begin[0:2],tid,number,linenum

def GetAllVideo(appkey,tid,begin,end,path):
  #  if os.path.exists('./%s/%d.txt'%(path,tid)):
   #     print './%s/%d.txt'%(path,tid),' Already exist'
    #    return
  #  f = open('./%s/%d.txt'%(path,tid),'w');
   # [pages,number,videolist] = GetRank(appkey,tid,order='hot',pagesize = 100,begin=begin,end=end,click_detail='true')
  #  for video in videolist:
  #      videowrite(f,video);
  #  if pages == 1 or len(videolist) == 0:
  #      print '    ',time.strftime('%H:%M:%S',time.localtime(time.time())),begin[0:2],tid,1,1
  #      f.close()
  #      return
  #  for page in range(2,pages+1):
   #     print '    ',time.strftime('%H:%M:%S',time.localtime(time.time())),begin[0:2],tid,page,'/',pages
    #    time.sleep(3)
    [page2,number2,videolist2] = GetRank(appkey,tid,order='hot',page=43,pagesize = 100,begin=begin,end=end,click_detail='true')
    for video in videolist2:
        print video.title,video.aid
 #           videowrite(f,video);
 #   f.close()
    return

def main():
    appkey = '03fc8eb101b091fb';
    for year in range(2013,2014):
        for month in range(11,12):
            begin = [year,month,2];
            if year == 2015 and month >= 1:
                continue;
            if year == 2009 and month < 6:
                continue
            if month == 12:
                end = [year+1,1,1]
            else:
                end = [year,month+1,1];
            path = '%d-%d'%(year,month);
            if not os.path.exists(path):
                os.mkdir(path)
            for tid in range(4,5):
                GetAllVideo(appkey,tid,begin,end,path)
#                 Check(appkey,tid,begin,end,path)

if __name__ == "__main__":
    main()
    print 'finished'
