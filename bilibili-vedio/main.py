# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 00:00:22 2014

@author: Administrator
"""


from bilibili import * 
import os

def vediowrite(f,vedio):
    f.write('Aid:%s\nTitle:%s\n'%(vedio.aid,vedio.title.encode('gbk','ignore')))
    f.write('Typeid:%s\nTypename:%s\n'%(vedio.tid,vedio.typename))
    f.write('Click:%s\nDanmu:%s\n'%(vedio.guankan,vedio.danmu))
    f.write('comment:%s\n'%(vedio.commentNumber))
    f.write('favorite:%s\n'%(vedio.shoucang))
    f.write('author:%s %s\n'%(vedio.author.name.encode('gbk','ignore'),vedio.author.mid))
    f.write('date:%s\n'%(vedio.date))
    f.write('credit:%s\n'%(vedio.credit))
    f.write('coin:%s\n'%(vedio.coin))
    f.write('duration:%s\n'%(vedio.duration))
    f.write('play_site:%s\n'%(vedio.play_site))
    f.write('play_forward:%s\n'%(vedio.play_forward))
    f.write('play_mobile:%s\n'%(vedio.play_mobile))
    f.write('\n')

def GetAllVedio(appkey,tid,begin,end,path):
    f = open('./%s/%d.txt'%(path,tid),'w');
    [pages,name,vediolist] = GetRank(appkey,tid,order='hot',pagesize = 100,begin=begin,end=end,click_detail='true')    
    if pages == 1 or len(vediolist) == 0:
        for vedio in vediolist:
            vediowrite(f,vedio);
        f.close()
        return
    for page in range(2,pages+1):
        print begin,end,tid,page,pages
        time.sleep(5)
        [page2,name2,vediolist2] = GetRank(appkey,tid,order='hot',page=page,pagesize = 100,begin=begin,end=end,click_detail='true')
        for vedio in vediolist2:
            vediowrite(f,vedio);
    f.close()
    return

def main():
    appkey = 'xxx';
    for year in [2012,2015]:
        for month in range(1,13):
            begin = [year,month,2];
            if year == 2014 and month >= 7:
                continue;
            if month == 12:
                end = [year+1,1,1]
            else:
                end = [year,month+1,1];
            path = '%d-%d'%(year,month);
            if not os.path.exists(path):
                os.mkdir(path)
            for tid in range(1,114):
                 GetAllVedio(appkey,tid,begin,end,path)

if __name__ == "__main__":
    main()
    print 'finished'