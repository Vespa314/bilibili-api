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
    f.close;
    return result

def main():
    try:
        f = open('bilibili-relation.txt','a+')
        polist = readfile('polist.txt')
        finished = readfile('finished.txt');
        idx = 0;
        while polist != []:
            cur = polist.pop(0);
            finished.append(cur);
            user = GetUserInfoBymid(cur);
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
                print 'finished:',idx;
                print 'left:',len(polist);
#                time.sleep(1);
        f.close();
    except:
        f.write('++++++++++++++++++++++')
        pofile = open('polist.txt')
        for item in polist:
            pofile.write(str(item)+'\n');
        pofile.close();
        pofile = open('finished.txt')
        for item in finished:
            pofile.write(str(item)+'\n');
        pofile.close();
        f.close();
#        main()

if __name__ == "__main__":
    main();
