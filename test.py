import cv2
import numpy as np

# 開啟網路攝影機
cap = cv2.VideoCapture(1)

# 設定影像尺寸
width = 840
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
t1 = cap.read()[1]
markColor=(0,255,0)
frameSum = np.zeros((height,width,3), np.uint8)
while(True):
    t0 = t1
    t1 = cap.read()[1]

    frameDelta = cv2.absdiff(t1, t0)
    frameDeltaGray = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',frameDeltaGray)

    k = cv2.waitKey(1) # 1msec待つ

    if (k == 27): # ESCキーで終了
        break

cap.release()
cv2.destroyAllWindows()
