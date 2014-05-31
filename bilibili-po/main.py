# -*- coding: utf-8 -*-
"""
Created on Thu May 29 02:14:57 2014

@author: Administrator
"""

from bilibili import * 

def readfile(filename):
    result = [];
    f = open(filename,'r')
    for line in f:
        result.append(int(line));
    f.close();
    return result

def main():
    try:
        f = open('bilibili-relation.txt','a+')
        polist = readfile('polist.txt')
        finished = readfile('finished.txt');
        idx = 0;
        while polist != []:
            cur = polist.pop(0);
            print '\t',idx,len(polist),cur;
            finished.append(cur);
            user = GetUserInfoBymid(cur);
            if user == None:
                continue
            if user.article > 0:
                print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()));
                f.write('Up:%s %d\n'%(user.name,user.mid));
                f.write('fans:%d\n'%user.fans)
                f.write('article:%d\n'%user.article)
                for follow in user.followlist:
                    f.write('\t%d\n'%follow);
                    if not follow in finished:
                        if not follow in polist:
                            polist.append(follow);
                f.write('\n')
                idx += 1;
                time.sleep(0.5);
        f.close();
    except e:
        print str(e)
        #出错的话保持现场
        pofile = open('polist.txt','w')
        for item in polist:
            pofile.write(str(item)+'\n');
        pofile.close();
        pofile = open('finished.txt','w')
        for item in finished:
            pofile.write(str(item)+'\n');
        pofile.close();
        f.close();

if __name__ == "__main__":
    main();
