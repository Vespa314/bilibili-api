# -*- coding: utf-8 -*-
"""
Created on Mon May 26 23:42:03 2014

@author: Administrator
"""


from support import *
import hashlib
import io
import xml.dom.minidom
import random
import math
import os
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class safe_list(list):
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default

# Calculation is based on https://github.com/jabbany/CommentCoreLibrary/issues/5#issuecomment-40087282
#                     and https://github.com/m13253/danmaku2ass/issues/7#issuecomment-41489422
# ASS FOV = width*4/3.0
# But Flash FOV = width/math.tan(100*math.pi/360.0)/2 will be used instead
# Result: (transX, transY, rotX, rotY, rotZ, scaleX, scaleY)
def ConvertFlashRotation(rotY, rotZ, X, Y, width, height):
    def WrapAngle(deg):
        return 180-((180-deg) % 360)
    rotY = WrapAngle(rotY)
    rotZ = WrapAngle(rotZ)
    if rotY in (90, -90):
        rotY -= 1
    if rotY == 0 or rotZ == 0:
        outX = 0
        outY = -rotY  # Positive value means clockwise in Flash
        outZ = -rotZ
        rotY *= math.pi/180.0
        rotZ *= math.pi/180.0
    else:
        rotY *= math.pi/180.0
        rotZ *= math.pi/180.0
        outY = math.atan2(-math.sin(rotY)*math.cos(rotZ), math.cos(rotY))*180/math.pi
        outZ = math.atan2(-math.cos(rotY)*math.sin(rotZ), math.cos(rotZ))*180/math.pi
        outX = math.asin(math.sin(rotY)*math.sin(rotZ))*180/math.pi
    trX = (X*math.cos(rotZ)+Y*math.sin(rotZ))/math.cos(rotY)+(1-math.cos(rotZ)/math.cos(rotY))*width/2-math.sin(rotZ)/math.cos(rotY)*height/2
    trY = Y*math.cos(rotZ)-X*math.sin(rotZ)+math.sin(rotZ)*width/2+(1-math.cos(rotZ))*height/2
    trZ = (trX-width/2)*math.sin(rotY)
    FOV = width*math.tan(2*math.pi/9.0)/2
    try:
        scaleXY = FOV/(FOV+trZ)
    except ZeroDivisionError:
        logging.error('Rotation makes object behind the camera: trZ == %.0f' % trZ)
        scaleXY = 1
    trX = (trX-width/2)*scaleXY+width/2
    trY = (trY-height/2)*scaleXY+height/2
    if scaleXY < 0:
        scaleXY = -scaleXY
        outX += 180
        outY += 180
        logging.error('Rotation makes object behind the camera: trZ == %.0f < %.0f' % (trZ, FOV))
    return (trX, trY, WrapAngle(outX), WrapAngle(outY), WrapAngle(outZ), scaleXY*100, scaleXY*100)


def WriteCommentBilibiliPositioned(f, c, width, height, styleid):
    #BiliPlayerSize = (512, 384)  # Bilibili player version 2010
    #BiliPlayerSize = (540, 384)  # Bilibili player version 2012
    BiliPlayerSize = (672, 438)  # Bilibili player version 2014
    ZoomFactor = GetZoomFactor(BiliPlayerSize, (width, height))

    def GetPosition(InputPos, isHeight):
        isHeight = int(isHeight)  # True -> 1
        if isinstance(InputPos, int):
            return ZoomFactor[0]*InputPos+ZoomFactor[isHeight+1]
        elif isinstance(InputPos, float):
            if InputPos > 1:
                return ZoomFactor[0]*InputPos+ZoomFactor[isHeight+1]
            else:
                return BiliPlayerSize[isHeight]*ZoomFactor[0]*InputPos+ZoomFactor[isHeight+1]
        else:
            try:
                InputPos = int(InputPos)
            except ValueError:
                InputPos = float(InputPos)
            return GetPosition(InputPos, isHeight)

    try:
        comment_args = safe_list(json.loads(c[3]))
        text = ASSEscape(str(comment_args[4]).replace('/n', '\n'))
        from_x = comment_args.get(0, 0)
        from_y = comment_args.get(1, 0)
        to_x = comment_args.get(7, from_x)
        to_y = comment_args.get(8, from_y)
        from_x = GetPosition(from_x, False)
        from_y = GetPosition(from_y, True)
        to_x = GetPosition(to_x, False)
        to_y = GetPosition(to_y, True)
        alpha = safe_list(str(comment_args.get(2, '1')).split('-'))
        from_alpha = float(alpha.get(0, 1))
        to_alpha = float(alpha.get(1, from_alpha))
        from_alpha = 255-round(from_alpha*255)
        to_alpha = 255-round(to_alpha*255)
        rotate_z = int(comment_args.get(5, 0))
        rotate_y = int(comment_args.get(6, 0))
        lifetime = float(comment_args.get(3, 4500))
        duration = int(comment_args.get(9, lifetime*1000))
        delay = int(comment_args.get(10, 0))
        fontface = comment_args.get(12)
        isborder = comment_args.get(11, 'true')
        from_rotarg = ConvertFlashRotation(rotate_y, rotate_z, from_x, from_y, width, height)
        to_rotarg = ConvertFlashRotation(rotate_y, rotate_z, to_x, to_y, width, height)
        styles = ['\\org(%d, %d)' % (width/2, height/2)]
        if from_rotarg[0:2] == to_rotarg[0:2]:
            styles.append('\\pos(%.0f, %.0f)' % (from_rotarg[0:2]))
        else:
            styles.append('\\move(%.0f, %.0f, %.0f, %.0f, %.0f, %.0f)' % (from_rotarg[0:2]+to_rotarg[0:2]+(delay, delay+duration)))
        styles.append('\\frx%.0f\\fry%.0f\\frz%.0f\\fscx%.0f\\fscy%.0f' % (from_rotarg[2:7]))
        if (from_x, from_y) != (to_x, to_y):
            styles.append('\\t(%d, %d, ' % (delay, delay+duration))
            styles.append('\\frx%.0f\\fry%.0f\\frz%.0f\\fscx%.0f\\fscy%.0f' % (to_rotarg[2:7]))
            styles.append(')')
        if fontface:
            styles.append('\\fn%s' % ASSEscape(fontface))
        styles.append('\\fs%.0f' % (c[6]*ZoomFactor[0]))
        if c[5] != 0xffffff:
            styles.append('\\c&H%s&' % ConvertColor(c[5]))
            if c[5] == 0x000000:
                styles.append('\\3c&HFFFFFF&')
        if from_alpha == to_alpha:
            styles.append('\\alpha&H%02X' % from_alpha)
        elif (from_alpha, to_alpha) == (255, 0):
            styles.append('\\fad(%.0f,0)' % (lifetime*1000))
        elif (from_alpha, to_alpha) == (0, 255):
            styles.append('\\fad(0, %.0f)' % (lifetime*1000))
        else:
            styles.append('\\fade(%(from_alpha)d, %(to_alpha)d, %(to_alpha)d, 0, %(end_time).0f, %(end_time).0f, %(end_time).0f)' % {'from_alpha': from_alpha, 'to_alpha': to_alpha, 'end_time': lifetime*1000})
        if isborder == 'false':
            styles.append('\\bord0')
        f.write('Dialogue: -1,%(start)s,%(end)s,%(styleid)s,,0,0,0,,{%(styles)s}%(text)s\n' % {'start': ConvertTimestamp(c[0]), 'end': ConvertTimestamp(c[0]+lifetime), 'styles': ''.join(styles), 'text': text, 'styleid': styleid})
    except (IndexError, ValueError) as e:
        try:
            logging.warning(_('Invalid comment: %r') % c[3])
        except IndexError:
            logging.warning(_('Invalid comment: %r') % c)

# Result: (f, dx, dy)
# To convert: NewX = f*x+dx, NewY = f*y+dy
def GetZoomFactor(SourceSize, TargetSize):
    try:
        if (SourceSize, TargetSize) == GetZoomFactor.Cached_Size:
            return GetZoomFactor.Cached_Result
    except AttributeError:
        pass
    GetZoomFactor.Cached_Size = (SourceSize, TargetSize)
    try:
        SourceAspect = SourceSize[0]/SourceSize[1]
        TargetAspect = TargetSize[0]/TargetSize[1]
        if TargetAspect < SourceAspect:  # narrower
            ScaleFactor = TargetSize[0]/SourceSize[0]
            GetZoomFactor.Cached_Result = (ScaleFactor, 0, (TargetSize[1]-TargetSize[0]/SourceAspect)/2)
        elif TargetAspect > SourceAspect:  # wider
            ScaleFactor = TargetSize[1]/SourceSize[1]
            GetZoomFactor.Cached_Result = (ScaleFactor, (TargetSize[0]-TargetSize[1]*SourceAspect)/2, 0)
        else:
            GetZoomFactor.Cached_Result = (TargetSize[0]/SourceSize[0], 0, 0)
        return GetZoomFactor.Cached_Result
    except ZeroDivisionError:
        GetZoomFactor.Cached_Result = (1, 0, 0)
        return GetZoomFactor.Cached_Result


def WriteASSHead(f, width, height, fontface, fontsize, alpha, styleid):
    f.write(
'''
[Script Info]
; Script generated by Danmaku2ASS
; https://github.com/m13253/danmaku2ass
Script Updated By: Danmaku2ASS (https://github.com/m13253/danmaku2ass)
ScriptType: v4.00+
PlayResX: %(width)d
PlayResY: %(height)d
Aspect Ratio: %(width)d:%(height)d
Collisions: Normal
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: %(styleid)s, %(fontface)s, %(fontsize).0f, &H%(alpha)02XFFFFFF, &H%(alpha)02XFFFFFF, &H%(alpha)02X000000, &H%(alpha)02X000000, 0, 0, 0, 0, 100, 100, 0.00, 0.00, 1, %(outline).0f, 0, 7, 0, 0, 0, 0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
''' % {'width': width, 'height': height, 'fontface': fontface, 'fontsize': fontsize, 'alpha': 255-round(alpha*255), 'outline': max(fontsize/25.0, 1), 'styleid': styleid}
    )

def TestFreeRows(rows, c, row, width, height, bottomReserved, lifetime):
    res = 0
    rowmax = height-bottomReserved
    targetRow = None
    if c[4] in (1, 2):
        while row < rowmax and res < c[7]:
            if targetRow != rows[c[4]][row]:
                targetRow = rows[c[4]][row]
                if targetRow and targetRow[0]+lifetime > c[0]:
                    break
            row += 1
            res += 1
    else:
        try:
            thresholdTime = c[0]-lifetime*(1-width/(c[8]+width))
        except ZeroDivisionError:
            thresholdTime = c[0]-lifetime
        while row < rowmax and res < c[7]:
            if targetRow != rows[c[4]][row]:
                targetRow = rows[c[4]][row]
                try:
                    if targetRow and (targetRow[0] > thresholdTime or targetRow[0]+targetRow[8]*lifetime/(targetRow[8]+width) > c[0]):
                        break
                except ZeroDivisionError:
                    pass
            row += 1
            res += 1
    return res

def MarkCommentRow(rows, c, row):
    row = int(row)
    try:
        for i in range(row, int(row+math.ceil(c[7]))):
            rows[c[4]][i] = c
    except IndexError:
        pass

def ASSEscape(s):
    def ReplaceLeadingSpace(s):
        sstrip = s.strip(' ')
        slen = len(s)
        if slen == len(sstrip):
            return s
        else:
            llen = slen-len(s.lstrip(' '))
            rlen = slen-len(s.rstrip(' '))
            return ''.join(('\u2007'*llen, sstrip, '\u2007'*rlen))
    return '\\N'.join((ReplaceLeadingSpace(i) or ' ' for i in str(s).replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}').split('\n')))

def ConvertTimestamp(timestamp):
    timestamp = round(timestamp*100.0)
    hour, minute = divmod(timestamp, 360000)
    minute, second = divmod(minute, 6000)
    second, centsecond = divmod(second, 100)
    return '%d:%02d:%02d.%02d' % (int(hour), int(minute), int(second), int(centsecond))

def ConvertType2(row, height, bottomReserved):
    return height-bottomReserved-row

def FindAlternativeRow(rows, c, height, bottomReserved):
    res = 0
    for row in range(int(height-bottomReserved-math.ceil(c[7]))):
        if not rows[c[4]][row]:
            return row
        elif rows[c[4]][row][0] < rows[c[4]][res][0]:
            res = row
    return res

def ConvertColor(RGB, width=1280, height=576):
    if RGB == 0x000000:
        return '000000'
    elif RGB == 0xffffff:
        return 'FFFFFF'
    R = (RGB >> 16) & 0xff
    G = (RGB >> 8) & 0xff
    B = RGB & 0xff
    if width < 1280 and height < 576:
        return '%02X%02X%02X' % (B, G, R)
    else:  # VobSub always uses BT.601 colorspace, convert to BT.709
        ClipByte = lambda x: 255 if x > 255 else 0 if x < 0 else round(x)
        return '%02X%02X%02X' % (
            ClipByte(R*0.00956384088080656+G*0.03217254540203729+B*0.95826361371715607),
            ClipByte(R*-0.10493933142075390+G*1.17231478191855154+B*-0.06737545049779757),
            ClipByte(R*0.91348912373987645+G*0.07858536372532510+B*0.00792551253479842)
        )

def WriteComment(f, c, row, width, height, bottomReserved, fontsize, lifetime, styleid):
    text = ASSEscape(c[3])
    styles = []
    if c[4] == 1:
        styles.append('\\an8\\pos(%(halfwidth)d, %(row)d)' % {'halfwidth': width/2, 'row': row})
    elif c[4] == 2:
        styles.append('\\an2\\pos(%(halfwidth)d, %(row)d)' % {'halfwidth': width/2, 'row': ConvertType2(row, height, bottomReserved)})
    elif c[4] == 3:
        styles.append('\\move(%(neglen)d, %(row)d, %(width)d, %(row)d)' % {'width': width, 'row': row, 'neglen': -math.ceil(c[8])})
    else:
        styles.append('\\move(%(width)d, %(row)d, %(neglen)d, %(row)d)' % {'width': width, 'row': row, 'neglen': -math.ceil(c[8])})
    if not (-1 < c[6]-fontsize < 1):
        styles.append('\\fs%.0f' % c[6])
    if c[5] != 0xffffff:
        styles.append('\\c&H%s&' % ConvertColor(c[5]))
        if c[5] == 0x000000:
            styles.append('\\3c&HFFFFFF&')
    ## 替换空格
    text = text.replace('\u2007',' ')
    f.write('Dialogue: 2,%(start)s,%(end)s,%(styleid)s,,0000,0000,0000,,{%(styles)s}%(text)s\n' % {'start': ConvertTimestamp(c[0]), 'end': ConvertTimestamp(c[0]+lifetime), 'styles': ''.join(styles), 'text': text, 'styleid': styleid})


def CalculateLength(s):
    return max(map(len, s.split('\n')))  # May not be accurate

def GetVideoInfo(aid,appkey,page = 1,AppSecret=None,fav = None):
    paras = {'id': GetString(aid),'page': GetString(page)}
    if fav != None:
        paras['fav'] = fav
    url =  'http://api.bilibili.cn/view?'+GetSign(paras,appkey,AppSecret)
    jsoninfo = JsonInfo(url)
    video = Video(aid,jsoninfo.Getvalue('title'))
    video.guankan = jsoninfo.Getvalue('play')
    video.commentNumber = jsoninfo.Getvalue('review')
    video.danmu = jsoninfo.Getvalue('video_review')
    video.shoucang = jsoninfo.Getvalue('favorites')
    video.description = jsoninfo.Getvalue('description')
    video.tag = []
    taglist = jsoninfo.Getvalue('tag')
    if taglist != None:
        for tag in taglist.split(','):
            video.tag.append(tag)
    video.cover = jsoninfo.Getvalue('pic')
    video.author = User(jsoninfo.Getvalue('mid'),jsoninfo.Getvalue('author'))
    video.page = jsoninfo.Getvalue('pages')
    video.date = jsoninfo.Getvalue('created_at')
    video.credit = jsoninfo.Getvalue('credit')
    video.coin = jsoninfo.Getvalue('coins')
    video.spid = jsoninfo.Getvalue('spid')
    video.cid = jsoninfo.Getvalue('cid')
    video.offsite = jsoninfo.Getvalue('offsite')
    video.partname = jsoninfo.Getvalue('partname')
    video.src = jsoninfo.Getvalue('src')
    video.tid = jsoninfo.Getvalue('tid')
    video.typename = jsoninfo.Getvalue('typename')
    video.instant_server = jsoninfo.Getvalue('instant_server')
    return video

def GetSign(params,appkey,AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
待添加：【重要！】
    需要做URL编码并保证字母都是大写，如 %2F
    """
    params['appkey']=appkey
    data = ""
    paras = params.keys()
    paras.sort()
    for para in paras:
        if data != "":
            data += "&"
        data += para + "=" + params[para]
    if AppSecret == None:
        return data
    m = hashlib.md5()
    m.update(data+AppSecret)
    return data+'&sign='+m.hexdigest()




def GetDanmuku(cid):
    cid = getint(cid)
    url = "http://comment.bilibili.cn/%d.xml"%(cid)
    content = zlib.decompressobj(-zlib.MAX_WBITS).decompress(getURLContent(url))
#    content = GetRE(content,r'<d p=[^>]*>([^<]*)<')
    return content


#def FilterBadChars(f):
#    s = f.read()
#    s = re.sub('[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]', '\ufffd', s)
#    return io.StringIO(s)

def ReadCommentsBilibili(f, fontsize):
    dom = xml.dom.minidom.parseString(f)
    comment_element = dom.getElementsByTagName('d')
    for i, comment in enumerate(comment_element):
        try:
            p = str(comment.getAttribute('p')).split(',')
            assert len(p) >= 5
            assert p[1] in ('1', '4', '5', '6', '7')
            if p[1] != '7':
                c = str(comment.childNodes[0].wholeText).replace('/n', '\n')
                size = int(p[2])*fontsize/25.0
                yield (float(p[0]), int(p[4]), i, c, {'1': 0, '4': 2, '5': 1, '6': 3}[p[1]], int(p[3]), size, (c.count('\n')+1)*size, CalculateLength(c)*size)
            else:  # positioned comment
                c = str(comment.childNodes[0].wholeText)
                yield (float(p[0]), int(p[4]), i, c, 'bilipos', int(p[3]), int(p[2]), 0, 0)
        except (AssertionError, AttributeError, IndexError, TypeError, ValueError):
            continue

def ConvertToFile(filename_or_file, *args, **kwargs):
    return open(filename_or_file, *args, **kwargs)


def ProcessComments(comments, f, width, height, bottomReserved, fontface, fontsize, alpha, lifetime, reduced, progress_callback):
    styleid = 'Danmaku2ASS_%04x' % random.randint(0, 0xffff)
    WriteASSHead(f, width, height, fontface, fontsize, alpha, styleid)
    rows = [[None]*(height-bottomReserved+1) for i in range(4)]
    for idx, i in enumerate(comments):
        if progress_callback and idx % 1000 == 0:
            progress_callback(idx, len(comments))
        if isinstance(i[4], int):
            row = 0
            rowmax = height-bottomReserved-i[7]
            while row <= rowmax:
                freerows = TestFreeRows(rows, i, row, width, height, bottomReserved, lifetime)
                if freerows >= i[7]:
                    MarkCommentRow(rows, i, row)
                    WriteComment(f, i, row, width, height, bottomReserved, fontsize, lifetime, styleid)
                    break
                else:
                    row += freerows or 1
            else:
                if not reduced:
                    row = FindAlternativeRow(rows, i, height, bottomReserved)
                    MarkCommentRow(rows, i, row)
                    WriteComment(f, i, row, width, height, bottomReserved, fontsize, lifetime, styleid)
        elif i[4] == 'bilipos':
            WriteCommentBilibiliPositioned(f, i, width, height, styleid)
        elif i[4] == 'acfunpos':
            WriteCommentAcfunPositioned(f, i, width, height, styleid)
        elif i[4] == 'sH5Vpos':
            WriteCommentSH5VPositioned(f, i, width, height, styleid)
        else:
            logging.warning(_('Invalid comment: %r') % i[3])
    if progress_callback:
        progress_callback(len(comments), len(comments))

def ReadComments(input_files, font_size=25.0):
    comments = []
    comments.extend(ReadCommentsBilibili(input_files, font_size))
    comments.sort()
    return comments

