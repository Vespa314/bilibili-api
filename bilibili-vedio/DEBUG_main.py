# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 00:00:22 2014

@author: Administrator
"""
from bilibili import *
import os

def vediowrite(f,vedio):
    
    f.write('Aid:%s\nTitle:%s\n'%(vedio.aid.encode('utf8'),vedio.title.encode('utf8')))
    f.write('copyright:%s\n'%(vedio.Iscopy.encode('utf8')))
    f.write('Typeid:%s\nTypename:%s\n'%(vedio.tid,vedio.typename.encode('utf8')))
    f.write('Click:%s\nDanmu:%s\n'%(vedio.guankan,vedio.danmu))
    f.write('comment:%s\n'%(vedio.commentNumber))
    f.write('favorite:%s\n'%(vedio.shoucang))
    if vedio.author.name:
        f.write('author:%s %s\n'%(vedio.author.name.encode('utf8'),vedio.author.mid))
    else:
        f.write('author:%s %s\n'%('NULL',vedio.author.mid))
    f.write('date:%s\n'%(vedio.date))
    f.write('credit:%s\n'%(vedio.credit))
    f.write('coin:%s\n'%(vedio.coin))
    f.write('duration:%s\n'%(vedio.duration))
    f.write('play_site:%s\n'%(vedio.play_site))
    f.write('play_forward:%s\n'%(vedio.play_forward))
    f.write('play_mobile:%s\n'%(vedio.play_mobile))
    f.write('\n')

def linecount_2(filename):
    count = -1 #让空文件的行号显示0
    for count,line in enumerate(open(filename,'r')):
        pass
    return count+1

def Check(appkey,tid,begin,end,path):
    filepath = './%s/%d.txt'%(path,tid)
    [pages,number,vediolist] = GetRank(appkey,tid,order='hot',pagesize = 100,begin=begin,end=end,click_detail='true')
    time.sleep(3)
    linenum = int(linecount_2(filepath)/17);
    print time.strftime('%H:%M:%S',time.localtime(time.time())),
    if number > linenum:
        if abs(number-linenum-len(vediolist)) < 5:
            print 'All 100:',begin[0:2],tid,number,linenum,len(vediolist)
            f = open('./%s/%d.txt'%(path,tid),'a+');
            for vedio in vediolist:
                vediowrite(f,vedio);
            f.close()
        else:
            print 'lose:',begin[0:2],tid,number,linenum
            GetAllVedio(appkey,tid,begin,end,path)
    elif number < linenum:
        print 'now lost:',begin[0:2],tid,number,linenum
    elif number == linenum:
        print 'match:',begin[0:2],tid,number,linenum

def GetAllVedio(appkey,tid,begin,end,path):
  #  if os.path.exists('./%s/%d.txt'%(path,tid)):
   #     print './%s/%d.txt'%(path,tid),' Already exist'
    #    return
  #  f = open('./%s/%d.txt'%(path,tid),'w');
   # [pages,number,vediolist] = GetRank(appkey,tid,order='hot',pagesize = 100,begin=begin,end=end,click_detail='true')
  #  for vedio in vediolist:
  #      vediowrite(f,vedio);
  #  if pages == 1 or len(vediolist) == 0:
  #      print '    ',time.strftime('%H:%M:%S',time.localtime(time.time())),begin[0:2],tid,1,1
  #      f.close()
  #      return
  #  for page in range(2,pages+1):
   #     print '    ',time.strftime('%H:%M:%S',time.localtime(time.time())),begin[0:2],tid,page,'/',pages
    #    time.sleep(3)
    [page2,number2,vediolist2] = GetRank(appkey,tid,order='hot',page=43,pagesize = 100,begin=begin,end=end,click_detail='true')
    for vedio in vediolist2:
        print vedio.title,vedio.aid
 #           vediowrite(f,vedio);
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
                GetAllVedio(appkey,tid,begin,end,path)
#                 Check(appkey,tid,begin,end,path)

if __name__ == "__main__":
    main()
    print 'finished'
