import cv2
import webbrowser
import time
import numpy as np


startTime = time.time()
lastTime = time.time()
doneTime = time.time()
# 開啟網路攝影機
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
BLOCKWIDTH = 180
PROGHEIGHT = 20
WAITTIME = 1

# 設定影像尺寸
width = 640
height = 360

# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 計算畫面面積
area = width * height

# 初始化平均影像
ret, frame = cap.read()
avg = cv2.blur(frame, (4, 4))
avg_float = np.float32(avg)
    
t0 = cap.read()[1]

markColor=(0,255,0)
frameSum = np.zeros((height,width,3), np.uint8)

# MOG2
fgbg = cv2.createBackgroundSubtractorMOG2(history = 1000)

# variables
flag = 0
counter = 0
b1 = 0
b2 = 0
b3 = 0
color = [0, 255, 0] 
changeColor = False
lastInstruct = -1
lastDoneInstruct = 0

while(True):
    t1 = t0
    t0 = cap.read()[1]
    
    # 切換顏色
    if changeColor == True:
        tmp = color[0]
        color[0] = color[2]
        color[2] = color[1]
        color[1] = tmp
        changeColor = False
        instruct = 0
        lastTime = time.time()
        
    # 在圖片上畫綠色方框，線條寬度為 2 px 
    cv2.rectangle(t1, (20, 20), (20+BLOCKWIDTH, 20+BLOCKWIDTH), (color[0], color[1], color[2]), 2) 
    cv2.rectangle(t1, (230, 20), (230+BLOCKWIDTH, 20+BLOCKWIDTH), (color[0], color[1], color[2]), 2)
    cv2.rectangle(t1, (440, 20), (440+BLOCKWIDTH, 20+BLOCKWIDTH), (color[0], color[1], color[2]), 2)

    # 左右翻轉frame
    t1 = cv2.flip(t1, 1)

    # 文字
    cv2.putText(t1, 'Exit', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[0], color[1], color[2]), 1, cv2.LINE_AA)
    cv2.putText(t1, 'Cange', (240, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[0], color[1], color[2]), 1, cv2.LINE_AA)
    cv2.putText(t1, 'Color', (240, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[0], color[1], color[2]), 1, cv2.LINE_AA)
    cv2.putText(t1, 'Google', (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[0], color[1], color[2]), 1, cv2.LINE_AA)

    
    
    fgmask = fgbg.apply(t1)

    # 前5幀容易出現偏差，從第6幀開始計算背景相減
    if time.time() - startTime > 5:

        # 計算共算存5幀的變化量
    
            # buttom1 Exit
        for row in range(20, 200):
            for col in range(20, 200):
                b1 += fgmask[row][col]
        # buttom2 變換顏色
        for row in range(20, 200):
            for col in range(230, 410):
                b2 += fgmask[row][col]
        # buttom3 開啟google
        for row in range(20, 200):
            for col in range(440, 620):
                b3 += fgmask[row][col]
        
        # 判斷經過5幀框格內的變化量是否超過threshold
        
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

        
        cv2.rectangle(t1, (20 - 1, 20+BLOCKWIDTH), (20+BLOCKWIDTH - 1, 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), 2)
        cv2.rectangle(t1, (230 - 1, 20+BLOCKWIDTH), (230+BLOCKWIDTH - 1, 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), 2)
        cv2.rectangle(t1, (440 - 1, 20+BLOCKWIDTH), (440+BLOCKWIDTH - 1, 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), 2)

        if lastDoneInstruct != instruct or time.time() - doneTime > WAITTIME:
            if(instruct == 1):
                cv2.rectangle(t1, (20, 20+BLOCKWIDTH), (min(20+(int)(BLOCKWIDTH * ((time.time() - lastTime) / WAITTIME)), 200), 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), -1)
            if(instruct == 2):
                cv2.rectangle(t1, (230, 20+BLOCKWIDTH), (min(230+(int)(BLOCKWIDTH * ((time.time() - lastTime) / WAITTIME)), 410), 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), -1)
            if(instruct == 3):
                cv2.rectangle(t1, (440, 20+BLOCKWIDTH), (min(440+(int)(BLOCKWIDTH * ((time.time() - lastTime) / WAITTIME)), 620), 20+BLOCKWIDTH+PROGHEIGHT), (color[0], color[1], color[2]), -1)


        print("instruct =", instruct, "time =", time.time() - lastTime, end = '\r')
        if time.time() - lastTime <= WAITTIME and instruct != 0:
            if lastInstruct != instruct or (lastDoneInstruct == instruct and time.time() - doneTime < WAITTIME):
                lastTime = time.time()
            lastInstruct = instruct
            instruct = -1
        else:
            lastTime = time.time()
        
        if instruct == 1:
            break
        if instruct == 2:
            changeColor = True
        if instruct == 3:
            url = 'https://www.google.com.tw/'
            webbrowser.open(url)
            instruct = 0
            lastTime = time.time()
        if instruct != 0 and instruct != -1:
            lastDoneInstruct = instruct
            doneTime = time.time()
    else:
        cv2.putText(t1, 'Wait for ' + (str)((int)(5 - (time.time() - startTime))) + ' to start.', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (color[0], color[1], color[2]), 1, cv2.LINE_AA)
        cv2.rectangle(t1, (20, 300), (620, 300+PROGHEIGHT), (color[0], color[1], color[2]), 2)
        cv2.rectangle(t1, (20, 300), (20+(int)(600 * ((time.time() - startTime) / 5)), 300+PROGHEIGHT), (color[0], color[1], color[2]), -1)
    
    cv2.imshow('frameori', t1)

    flag += 1
    
    cv2.imshow('frame',fgmask)

    k = cv2.waitKey(1) # 等1msec

    if (k == 27): # 按ESC跳出
        break

cap.release()
cv2.destroyAllWindows()