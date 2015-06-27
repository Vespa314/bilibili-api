## 说明

本模块主要可以通过输入B站视频链接获得由弹幕xml文件转换而成的ass字幕文件，供本地视频加载用

输入：
    av号
返回：
    在桌面获得视频同名ass文件
    
## 注意
代码暂时只在MAC系统下测试通过，对于其他系统可以自行研究，至少。。。。。下面这句代码的目标路径你要改一下吧。。。

```
Danmaku2ASS(GetDanmuku(video.cid),r'%s/Desktop/%s.ass'%(os.path.expanduser('~'),video.title), 640, 360, 0, 'sans-serif', 15, 0.5, 10, False)
```
如果有疑问想交流，可以电邮:`kylensherlock艾特gmail.com`


## 缺陷
暂时而言字母参数写死了，懒得通过外部修改

~~暂时不支持下载P2弹幕。。。后期会加上。。。~~ 【已支持】

##鸣谢

我只是写了一下B站api获得弹幕，而转换模块基本参考[m13253](https://github.com/m13253)所写的[danmaku2ass](https://github.com/m13253/danmaku2ass)项目！！！

> 做了些许修改。。。