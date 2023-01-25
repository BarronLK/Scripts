from MyQR import myqr
import os

str =  input('请输入:')
version, level, qr_name = myqr.run(
    words=str,
    version=1, 		
    level='H',		
    picture="1.jpg",
    colorized=True,		
    contrast=1.0,   		
    brightness=1.0, 		
    save_name="2.png",
    save_dir=os.getcwd()
)
os.system("pause")
