import cv2
import webbrowser
import time
import numpy as np
import random
import os

startTime = time.time()
lastTime = time.time()
doneTime = time.time()
# 開啟網路攝影機
cap = cv2.VideoCapture(0)

# 設定影像尺寸
width = 1280
height = 720

# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 初始化影像
t0 = cap.read()[1]

# MOG2
fgbg = cv2.createBackgroundSubtractorMOG2(history = 1000)

# variables
BLOCKWIDTH = 180
PROGHEIGHT = 20
WAITTIME = 2
flag = 0
counter = 0
b1 = 0
b2 = 0
b3 = 0
b4 = 0
color = [0, 255, 0] 
changeColor = False
lastInstruct = -1
lastDoneInstruct = 0

while(True):
    t1 = t0
    t0 = cap.read()[1]
    
    # 切換顏色
    if changeColor == True:
        color[0] = random.randint(0, 255)
        color[1] = random.randint(0, 255)
        color[2] = random.randint(0, 255)
        changeColor = False
        instruct = 0
        lastTime = time.time()
        
    # 左右翻轉frame
    t1 = cv2.flip(t1, 1)

    # 在圖片上畫綠色方框，線條寬度為 2 px 
    cv2.rectangle(t1, (20, 20), (20+BLOCKWIDTH, 20+BLOCKWIDTH), (color[0], color[1], color[2]), 2) 
    cv2.rectangle(t1, (230, 20), (230+BLOCKWIDTH, 20+BLOCKWIDTH), (color[0], color[1], color[2]), 2)
    cv2.rectangle(t1, (440, 20), (440+BLOCKWIDTH, 20+BLOCKWIDTH), (color[0], color[1], color[2]), 2)
    cv2.rectangle(t1, (650, 20), (650+BLOCKWIDTH, 20+BLOCKWIDTH), (color[0], color[1], color[2]), 2)

    # 文字
    cv2.putText(t1, 'Exit', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[2], color[1], color[0]), 1, cv2.LINE_AA)
    cv2.putText(t1, 'Change', (240, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[2], color[1], color[0]), 1, cv2.LINE_AA)
    cv2.putText(t1, 'Color', (240, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[2], color[1], color[0]), 1, cv2.LINE_AA)
    cv2.putText(t1, 'Google', (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[2], color[1], color[0]), 1, cv2.LINE_AA)
    cv2.putText(t1, 'Taskmgr', (660, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[2], color[1], color[0]), 1, cv2.LINE_AA)
    
    
    fgmask = fgbg.apply(t1)

    # 前幾幀容易出現偏差，等5秒在開始
    if time.time() - startTime > 5:
    
        # 計算變化量
        for row in range(20, 200):
            for col in range(20, 200):
                b1 += fgmask[row][col]
        for row in range(20, 200):
            for col in range(230, 410):
                b2 += fgmask[row][col]
        for row in range(20, 200):
            for col in range(440, 620):
                b3 += fgmask[row][col]
        for row in range(20, 200):
            for col in range(650, 830):
                b4 += fgmask[row][col]

        instruct = 0
        if b1 >((180 * 180 * 255) / 4):
            instruct = 1
        b1 = 0
        if b2 >((180 * 180 * 255) / 4):
            if instruct == 0:
                instruct = 2
            else:
                instruct = -1
        b2 = 0
        if b3 >((180 * 180 * 255) / 4):
            if instruct == 0:
                instruct = 3
            else:
                instruct = -1
        b3 = 0
        if b4 >((180 * 180 * 255) / 4):
            if instruct == 0:
                instruct = 4
            else:
                instruct = -1
        b4 = 0
        
        # 顯示讀條
        cv2.rectangle(t1, (20, 20+BLOCKWIDTH), (20+BLOCKWIDTH, 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), 2)
        cv2.rectangle(t1, (230, 20+BLOCKWIDTH), (230+BLOCKWIDTH, 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), 2)
        cv2.rectangle(t1, (440, 20+BLOCKWIDTH), (440+BLOCKWIDTH, 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), 2)
        cv2.rectangle(t1, (650, 20+BLOCKWIDTH), (650+BLOCKWIDTH, 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), 2)


        if lastDoneInstruct != instruct or time.time() - doneTime > WAITTIME:
            if(instruct == 1):
                cv2.rectangle(t1, (20, 20+BLOCKWIDTH), (min(20+(int)(BLOCKWIDTH * ((time.time() - lastTime) / WAITTIME)), 200), 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), -1)
            if(instruct == 2):
                cv2.rectangle(t1, (230, 20+BLOCKWIDTH), (min(230+(int)(BLOCKWIDTH * ((time.time() - lastTime) / WAITTIME)), 410), 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), -1)
            if(instruct == 3):
                cv2.rectangle(t1, (440, 20+BLOCKWIDTH), (min(440+(int)(BLOCKWIDTH * ((time.time() - lastTime) / WAITTIME)), 620), 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), -1)
            if(instruct == 4):
                cv2.rectangle(t1, (650, 20+BLOCKWIDTH), (min(650+(int)(BLOCKWIDTH * ((time.time() - lastTime) / WAITTIME)), 830), 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), -1)


        print("instruct =", instruct, "time =", time.time() - lastTime, end = '\r')
        if time.time() - lastTime <= WAITTIME and instruct != 0:
            if lastInstruct != instruct or (lastDoneInstruct == instruct and time.time() - doneTime < WAITTIME):
                lastTime = time.time()
            lastInstruct = instruct
            instruct = -1
        else:
            lastTime = time.time()
        
        # buttom1 Exit
        if instruct == 1:
            break
        # buttom2 變換顏色
        if instruct == 2:
            changeColor = True
        # buttom3 開啟google
        if instruct == 3:
            url = 'https://www.google.com.tw/'
            webbrowser.open(url)
        if instruct == 4:
            os.popen('taskmgr')
            
        if instruct != 0 and instruct != -1:
            lastDoneInstruct = instruct
            doneTime = time.time()
    else:
        cv2.putText(t1, 'Wait for ' + (str)((int)(5 - (time.time() - startTime))) + ' to start.', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[0], color[1], color[2]), 1, cv2.LINE_AA)
        cv2.rectangle(t1, (20, 300), (830, 300+PROGHEIGHT), (color[0], color[1], color[2]), 2)
        cv2.rectangle(t1, (20, 300), (20+(int)(810 * ((time.time() - startTime) / 5)), 300+PROGHEIGHT), (color[0], color[1], color[2]), -1)
    
    cv2.imshow('frameori', t1)

    flag += 1
    
    cv2.imshow('frame',fgmask)

    k = cv2.waitKey(1) # 等1msec

    if (k == 27): # 按ESC跳出
        break

cap.release()
cv2.destroyAllWindows()