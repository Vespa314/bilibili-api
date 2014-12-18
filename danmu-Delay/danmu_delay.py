# 对ass弹幕文件进行延时。。。
# 为什么会有这个需求呢？因为妈蛋ffmpeg剪切ts视频失败啊！！
# 只好弹幕来配合了。。。
# 如果以后经常遇到。。再整理得好用一些。。。
# 酱~

import re

def t_delay(h,m,s,delay):
    s += delay;
    if s >= 60:
        s -= 60
        m += 1
        if m >= 60:
            m -= 60
            h += 1
    return [h,m,s]

filename = r'in.ass'
delay = 30;
fid = open('out.ass','w')
for line in open(filename):
    t = re.findall(r'^(Dialogue: 2,)(\d+):(\d+):(\d+)\.(\d+),(\d+):(\d+):(\d+)\.(.*)$',line)
    if len(t) == 0:
        fid.write(line)
    else:
        t = t[0]       
        [h,m,s] = t_delay(int(t[1]),int(t[2]),int(t[3]),delay)      
        fid.write('%s%d:%.2d:%.2d.%s,'%(t[0],h,m,s,t[4]))        
        [h,m,s] = t_delay(int(t[5]),int(t[6]),int(t[7]),delay) 
        fid.write('%d:%.2d:%.2d.%s\n'%(h,m,s,t[8]))
        
fid.close();
print "finished!!"


