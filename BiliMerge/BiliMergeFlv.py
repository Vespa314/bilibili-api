#!/usr/bin/env python

import subprocess
import os
import sys
import glob

def merge(folder):
    flv_list = sorted(glob.glob('{folder}/*.flv'.format(folder = folder)))
    fid = open('%s/filelist.txt' % (folder), 'w')
    for idx in flv_list:
        fid.write("file '%s/%d.flv'\n" % (folder, idx))
    fid.close()
    
    cmd = ['ffmpeg', '-f', 'concat', '-i', folder+'/'+'filelist.txt','-codec', 'copy', folder+'/'+'output.mp4']
    subprocess.Popen(cmd).wait()

if __name__ == "__main__":
    merge(sys.argv[1]);