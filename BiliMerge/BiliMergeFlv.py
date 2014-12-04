#!/usr/bin/env python

import subprocess
import os 
import sys

def merge(dir):
    fid = open('%s/filelist.txt'%(dir),'w')
    for idx in xrange(0,10000):
        if os.path.isfile('%s/%d.flv'%(dir,idx)):
            fid.write("file '%s/%d.flv'\n"%(dir,idx))
        else:
            break;
    fid.close()
    
    cmd = ['ffmpeg', '-f', 'concat', '-i', dir+'/'+'filelist.txt','-codec', 'copy', dir+'/'+'output.mp4']
    subprocess.Popen(cmd).wait()

if __name__ == "__main__":
    merge(sys.argv[1]);