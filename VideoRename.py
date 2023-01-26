#功能：遍历当前或指定文件夹下视频并重命名为'字母+数字'
import os

mediaext = ['mp4','m4v','mov','avi','flv','wmv','mkv','mpeg','vob','mpg','rm','rmvb','ts']
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
            if os.path.splitext(eachname)[-1][1:].lower() in mediaext:
                filepathpack = [os.path.join(currentdir,eachname),os.path.normpath(currentdir)] #[全路径文件名，全路径目录名]
                files.append(filepathpack)

    if pathcheck == False:
        raise
    if len(files) == 0 :
        raise ValueError()

    return(files) #输出 [[全路径文件名1，全路径目录名1],...]

def rename_mediafiles(files,name):
    files = files
    for fileindex,file in enumerate(files):
        oldname = file[0]
        newname = ''.join([name,str(fileindex+1),os.path.splitext(oldname)[-1]])
        newname = os.path.join(file[1],newname)
        os.rename(oldname,newname)


newname = input('视频并重命名为"字母+数字"格式，请输入字母：')
try:
    mediafiles = get_mediafiles(input('（可选）请输入指定路径：'))
    print('获取到',len(mediafiles),'个视频')
except ValueError:
    print('没有找到视频')
except:
    print('输入路径错误')
else:
    rename_mediafiles(mediafiles,newname)
    print('重命名完成')