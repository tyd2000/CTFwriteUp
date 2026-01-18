import requests
from lxml import html
import cv2
import numpy as np
import json

url="http://ede1b99e-ee29-4621-99c7-c97de218c1fc.challenge.ctf.show/"

sess=requests.session()

all_girl=sess.get(url+'/static/all_girl.png').content

with open('all_girl.png','wb')as f:
        f.write(all_girl)

big_pic=cv2.imdecode(np.fromfile('all_girl.png', dtype=np.uint8), cv2.IMREAD_UNCHANGED)
big_pic=big_pic[50:,50:,:]
image_alpha = big_pic[:, :, 3]
mask_img=np.zeros((big_pic.shape[0],big_pic.shape[1]), np.uint8)
mask_img[np.where(image_alpha == 0)] = 255

cv2.imwrite('big.png',mask_img)

def answer_one(sess):
        #获取视频文件
        response=sess.get(url+'/check')
        if 'ctfshow{' in response.text:
                print(response.text)
                exit(0)
        tree=html.fromstring(response.text)
        element=tree.xpath('//source[@id="vsource"]')
        video_path=element[0].get('src')
        video_bin=sess.get(url+video_path).content
        with open('Question.mp4','wb')as f:
                f.write(video_bin)
        #获取有效帧
        video = cv2.VideoCapture('Question.mp4')
        frame=0
        while frame<=55:
                res, image = video.read()
                frame+=1
        #cv2.imwrite('temp.png',image)
        video.release()
        #获取剪影
        image=image[100:400,250:500]
        gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #cv2.imwrite('gray_image.png',gray_image)
        temp = np.zeros((300, 250), np.uint8)
        temp[np.where(gray_image>=128)]=255
        #去白边
        temp = temp[[not np.all(temp[i] == 255) for i in range(temp.shape[0])], :]
        temp = temp[:, [not np.all(temp[:, i] == 255) for i in range(temp.shape[1])]]
        #缩放至合适大小，肉眼大致判断是1.2倍，不一定准
        temp = cv2.resize(temp,None,fx=1.2,fy=1.2)
        #查找位置
        res =cv2.matchTemplate( mask_img,temp,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        x,y=int(max_loc[0]/192),int(max_loc[1]/288)#为什么是192和288，因为大图去掉标题栏就是1920*2880
        guess='ABCDEFGHIJ'[y]+'0123456789'[x]
        print(f'guess:{guess}')
        #传答案
        response=sess.get(url+'/submit?guess='+guess)
        r=json.loads(response.text)
        if r['result']:
                print('guess right!')
                return True
        else:
                print('guess wrong!')
                return False

i=1

while i<=31:
        print(f'Round:{i}')
        if answer_one(sess):
                i+=1
        else:
                i=1