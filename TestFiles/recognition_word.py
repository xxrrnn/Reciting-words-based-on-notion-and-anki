import time

import cv2
import numpy as np
import pyautogui

import pywinauto.mouse
time.sleep(5)
# pyautogui.click(800,500, clicks=1, interval=0.25)

# pywinauto.mouse.scroll((800,300),-1) #(1100,300)是初始坐标，1000是滑动距离（可负）
def center(pos):
    pos_array = np.array(pos)
    print(pos_array)
    print(pos_array[:,1])
    print(pos_array[:,0])
    y = (np.max(pos_array[:,1]) + np.min(pos_array[:,1]))/2
    x = (np.max(pos_array[:,0]) + np.min(pos_array[:,0]))/2
    print("center",x,y)
    return (x,y)


notion_position = pyautogui.locateOnScreen('notion.png', grayscale=True, confidence= 0.7)

# notion_center = pyautogui.center(notion_position)
# pyautogui.click(notion_center, clicks=1, interval=0.25)

im2 = pyautogui.screenshot('my_screenshot.png')
img = cv2.imread("my_screenshot.png")

#转到HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print(hsv)

#设置阈值
l_blue = np.array([[0,43,46]])
h_blue = np.array([25,255,255])

#构建掩模
mask = cv2.inRange(hsv, l_blue, h_blue)

#进行位运算
res = cv2.bitwise_and(img, img, mask = mask)
cv2.imwrite("result.png",res)
# cv2.imshow("img", img)
# cv2.imshow("mask", mask)
# cv2.imshow("res", res)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import paddleocr

# 模型路径下必须含有model和params文件，如果没有，现在可以自动下载了，不过是最简单的模型
# use_gpu 如果paddle是GPU版本请设置为 True
ocr = paddleocr.PaddleOCR(use_angle_cls=True, use_gpu=True)

img_path = "result.png"  # 这个是自己的图片，自行放置在代码目录下修改名称

result = ocr.ocr(img_path, cls=True)
# for line in result:
#     print(line)
# 显示结果
from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0][1]  for line in result]
scores = [line[1][1]for line in result]
# im_show = draw_ocr(image, boxes, txts, scores)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')  # 结果图片保存在代码同级文件夹中。
# print("result",result)
pos = []
word = []
scores = []
img_res = cv2.imread("result.png")
height_img,width_img,_ = img_res.shape
print(height_img, width_img)
for lines in result:
    for line in lines:
        print("pos",line[0])
        pos.append(line[0])
        print("word + scores",line[1])
        word.append(line[1][0])
        scores.append(line[1][1])
for i in range(len(word)):
    if scores[i] > 0.9 :
        heights = [height[1] for height in pos[i]]
        # print(heights)
        if height_img - max(heights) > height_img /10 and min(heights) > height_img/10:
            print(word[i])
            word_pos = center(pos[i])

            # pyautogui.click(word_pos[0],word_pos[1], clicks=2, interval=0.25)


