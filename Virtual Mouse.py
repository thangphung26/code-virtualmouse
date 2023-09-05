import cv2
import numpy as np
import time
import HandTracking as ht
import autopy   
import pyautogui

pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 8         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)


detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max
screen_width, screen_height = autopy.screen.size()      # Getting the screen size
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting position of hand

    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        x0, y0 = lmlist[4][1:]

        fingers = detector.fingersUp()      # Check xem có phát hiện tay không
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   
        if fingers[1] == 1 and fingers[2] == 0:     # ngón trỏ up và ngón giữa down
            x6 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
            y6 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (x6 - prev_x)/smoothening
            curr_y = prev_y + (y6 - prev_y) / smoothening

            autopy.mouse.move(screen_width - curr_x, curr_y)    # Moving the cursor
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y
                    

        if fingers[1] == 1 and fingers[2] == 1:     # nếu ngón trỏ và ngón giữa cùng up
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:     # nếu khoảng cách giữa 2 ngón nhỏ hơn 40
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()    # Click chuột trái

        if fingers[1]== 1 and fingers[2]== 1 and fingers[0]==0:
            # cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            pyautogui.scroll(30)    # cuộn chuột lên

        if fingers[1]==0 and fingers[2]== 0:
            pyautogui.scroll(-30)       # cuộn chuột xuống

        if fingers[0]== 0 and fingers[1] == 1:  # nếu ngón cái dơ ra và ngón trỏ up
            length, img, lineInfo = detector.findDistance(8, 4, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)   # click chuột phải

        if fingers[1]== 1 and fingers[2]== 1 and fingers[0]==0:  # nếu ngón trỏ và ngón giữa cùng up
            # print("No")
            # length, img, lineInfo = detector.findDistance(4, 20, img)
            # if length > 100:
                min_scroll_interval = 0.5
                last_scroll_time = time.time()
                current_time = time.time()
                if current_time - last_scroll_time >= min_scroll_interval:
                    pyautogui.keyDown('ctrl')
                    pyautogui.scroll(3)         # nhấn ctrl để zoom in
                    pyautogui.keyUp('ctrl') 
                    last_scroll_time = current_time
                time.sleep(0.01)
        if fingers[1]== 0 and fingers[2]== 0:   # nếu ngón trỏ và ngón giữa cùng down
            min_scroll_interval = 0.5
            last_scroll_time = time.time()
            current_time = time.time()
            if current_time - last_scroll_time >= min_scroll_interval:
                pyautogui.keyDown('ctrl')
                pyautogui.scroll(-3)            # nhấn ctrl để zoom out
                pyautogui.keyUp('ctrl') 
                last_scroll_time = current_time
            time.sleep(0.01)
            # print("yes")
           
                  


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == 27:
        break
