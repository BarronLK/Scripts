from MyQR import myqr
import os
myqr.run(words = input("请输入："),save_name="qrcode.png",save_dir="./")
os.system("pause")
