import cv2 #getting frames from cam
import mediapipe as mp #detect landmarks of hand
import pyautogui #send key inputs to media player
import time #provides time to user

#list of all the keypoints of the hands
def count_fingers(lst):
    #track the count of number of fingers raised
    cnt = 0

    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

    if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 5:
        cnt += 1

    return cnt

#created cap object of videocapture to read frames from webcam
cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils #drawing keypoints of the hand on the frame
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1) #object of hand(limit of hand 1)

start_init = False

prev = -1
#infinite true loop
while True:
    end_time = time.time()
    #reading frames from cap(object)
    _, frm = cap.read()
    #fliping camera
    frm = cv2.flip(frm, 1)
    #opencv reads frames in bgr format (detect hands and sending to hand_obj)
    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    #returns list of hands detected on the frame
    if res.multi_hand_landmarks:
        #sometimes the value can be null
        hand_keyPoints = res.multi_hand_landmarks[0]
        #stores the result
        cnt = count_fingers(hand_keyPoints)

        if not (prev == cnt):
            if not (start_init):
                start_time = time.time()
                start_init = True
            #providing 0.2 secs to the user to perform the action
            elif (end_time - start_time) > 0.2:
                if (cnt == 1):
                    pyautogui.press("right")

                elif (cnt == 2):
                    pyautogui.press("left")

                elif (cnt == 3):
                    pyautogui.press("up")

                elif (cnt == 4):
                    pyautogui.press("down")

                elif (cnt == 5):
                    pyautogui.press("space")

                prev = cnt
                start_init = False
        #to draw landmarks,HAND_CONNECTIONS-used to connect the key points
        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)
    #window which is showing frame to the user
    cv2.imshow("window", frm)
    #waitkey waits for user to enter esc key to break out of the true loop
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        #releasing camera resource so that other applications can use it
        cap.release()
        break