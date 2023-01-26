#功能：遍历当前或指定文件夹下视频，依据视频时长创建内容缩略图，添加文件名及时长到图片
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

mediaext = ['mp4','m4v','mov','avi','flv','wmv','mkv','mpeg','vob','mpg','dat','rm','rmvb','ts']
workdir = ''

def get_mediafiles(opt_path):
    files = []
    global mediaext
    global workdir
    if opt_path == '':
        opt_path = os.path.dirname(os.path.abspath(__file__)) #.py文件路径
        pathcheck = True
    else:
        opt_path = os.path.abspath(opt_path) # 格式化路径
        pathcheck = os.path.exists(opt_path) # 检查路径存在性
    workdir = opt_path

    for currentdir,dirnames,filenames in os.walk(opt_path):
        for eachname in filenames:
            if os.path.splitext(eachname)[-1][1:].lower() in mediaext: #检查视频后缀名
                filepathpack = [os.path.join(currentdir,eachname),eachname,currentdir.replace(opt_path,'',1)] #[全路径文件名，文件全名，工作目录下目录路径]
                files.append(filepathpack)

    if pathcheck == False:
        raise
    if len(files) == 0 :
        raise ValueError()

    return(files) #输出 [[全路径文件名1，文件全名1，工作目录下路径1],...]

def get_frames_and_length(filepath):
    result = subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v',
        '-show_entries','stream=nb_read_frames,duration','-show_entries','format=duration',
        '-of','default=noprint_wrappers=1:nokey=1',filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT) 
    lengthandframes = result.stdout #输出 b'流时长秒\r\n帧数\r\n封装时长秒\r\n'
    lengthandframes = lengthandframes.splitlines() #输出 [b'流时长秒',b'帧数',b'封装时长秒']
    frames = int(lengthandframes[1])
    try:
        length = float(lengthandframes[0]) #测试mkv文件无法取得流时长
    except ValueError:
        length = float(lengthandframes[2])
    return(frames,length) #输出 int帧数 float时长秒
    
    #-v：设置库使用的日志记录级别和标志 
    #   quiet, -8：什么都不显示
    #   panic, 0：仅显示可能导致进程崩溃的致命错误，例如assertion failure，这目前不用于任何内容
    #   fatal, 8：仅显示致命错误，之后的过程绝对无法继续
    #   error, 16：显示所有错误，包括可以从中恢复的错误
    #   warning, 24：显示所有警告和错误
    #   info, 32：在处理过程中显示信息性消息，这是默认值
    #   verbose, 40：与info相同，只是更详细
    #   debug, 48：显示所有内容，包括调试信息
    #   trace, 56
    #-count_frames：计算每个流的帧数，并在相应的流部分中报告
    #-select_streams v:0 ：仅选择视频流
    #-show_entries stream = nb_read_frames ：只显示读取的帧数
    #-of default = nokey = 1：noprint_wrappers = 1 ：将输出格式(也称为“writer”)设置为默认值，不打印每个字段的键(nokey = 1)，不打印节头和页脚(noprint_wrappers = 1)
    
    #stdout、stderr：子进程的标准输出和错误，其值可以是 subprocess.PIPE、subprocess.DEVNULL、一个已经存在的文件描述符、已经打开的文件对象或者 None
    #subprocess.PIPE：为子进程创建新的管道
    #.splitlines() 按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，默认参数为False，不包含换行符

def get_picture_tile(time_in_seconds):
    if time_in_seconds <= 180:
        return '2x3',6
    elif time_in_seconds >180 and time_in_seconds <=450:
        return '3x5',15
    elif time_in_seconds >450 and time_in_seconds <=980:
        return '4x7',28
    elif time_in_seconds >980 and time_in_seconds <=1575:
        return '5x9',45
    elif time_in_seconds >1575 and time_in_seconds <=2700:
        return '6x10',60
    elif time_in_seconds >2700 and time_in_seconds <=3780:
        return '7x12',84
    else:
        return '8x14',112
     
    #2*3=6 3min 180s 30spf
    #3*5=15 7.5min 450s
    #4*7=28 16.3min 980s 35spf
    #5*9=45 26.3min 1575s
    #6*10=60 45min 2700s 45spf
    #7*12=84 63min 3780s
    #8*14=112

def generate_pictures(files):
    global workdir
    text_list = []
    
    try:
        os.mkdir(os.path.join(workdir,'VideoToPic_Output'))
    except:
        print('创建文件夹失败')

    for fileindex,file in enumerate(files):
        print('正在处理视频：',fileindex+1,'/',len(files))
        filepath = file[0]
        filefullname = file[1] # 文件名.扩展名
        outname = os.path.join(file[2],''.join([os.path.splitext(filefullname)[0],'.png'])) # \\目录\\文件名
        outname = outname.replace('\\','-') # -目录-文件名 Windows
        outname = outname.replace('/','-') # -目录-文件名 Linux
        outpath = os.path.join(workdir,'VideoToPic_Output',outname)

        frames,length = get_frames_and_length(filepath)
        tile,tile_numbers = get_picture_tile(length)
        sample_seconds = str(int(frames/tile_numbers))
        vf_argument = ''.join(['select=not(mod(n\,',sample_seconds,')),scale=240:-1,tile=',tile])

        text_list.append([outpath,int(length)])

        subprocess.run(['ffmpeg','-v','warning','-i',filepath,'-frames:v','1','-vf',vf_argument,outpath]) 
    return text_list

    #-vf "..." 筛选器
    #select='not(mod(n\,x))' 每x帧取1帧
    #scale=x:-1 按宽度x等比缩放
    #tile=axb 输出图像排列顺序是axb
    #-frames:v 设置要输出的视频帧数

def draw(picpath, text, left, top, text_color=(0, 0, 0), text_size=13):
    pyfilepath = os.path.dirname(os.path.abspath(__file__))
    fontpath = os.path.join(pyfilepath,'dengb.ttf') # 需要带有ttf字体
    fontStyle = ImageFont.truetype(fontpath, text_size, encoding="utf-8")

    picture = Image.open(picpath) # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(picture) 
    draw.text((left, top), text, text_color, font=fontStyle) # 绘制文本
    return picture

def generate_text(text_list):
    for pictureindex,picture in enumerate(text_list):
        print('正在添加文本：',pictureindex+1,'/',len(text_list))
        video_minutes = int(picture[1]/60)
        video_seconds = picture[1]%60
        if video_minutes == 0:
            video_length = ''.join([str(video_seconds),'s'])
        else:
            video_length = ''.join([str(video_minutes),'min',str(video_seconds),'s']) #转换视频长度到分钟

        picturepath = picture[0]
        picture_name = os.path.basename(picture[0])
        text = ' '.join([video_length,picture_name]) #输出 视频长度，图片文件名
        
        processed_picture1 = draw(picturepath, text, 5, 5, text_color=(0, 0, 0), text_size=35) #黑
        processed_picture1.save(picturepath)
        processed_picture2 = draw(picturepath, text, 5, 45, text_color=(255, 255, 255), text_size=35) #白
        processed_picture2.save(picturepath)

print('遍历当前或指定文件夹下视频，依据视频时长创建内容缩略图，添加文件名及时长到图片')
if input('是否添加时长及名称到缩略图？(Yy/Nn)').lower() == 'y':
    addtextbool = True
else:
    addtextbool = False

try:
    mediafiles = get_mediafiles(input('（可选）请输入指定路径：'))
    print('获取到',len(mediafiles),'个视频')
except ValueError:
    print('没有找到视频')
except:
    print('输入路径错误')
else:
    textlist = generate_pictures(mediafiles)
    print('缩略图创建完成')
    if addtextbool == True:
        generate_text(textlist)
        print('文字添加完成')