import cv2
import numpy as np
from tkinter import *
from threading import Thread
import queue
#from PIL import ImageTk, Image

huelower = 0
satlower = 0
valuelower = 0
hueupper = 0
satupper = 0
valueupper = 0


huelow_q = queue.Queue()
satlow_q = queue.Queue()
valuelow_q = queue.Queue()
hueup_q = queue.Queue()
satup_q = queue.Queue()
valueup_q = queue.Queue()

snapshot_pass = queue.Queue()


class gui(Thread):
    """docstring for ClassName"""
    def __init__(self):
        super(gui, self).__init__()

    def run(self):
        global huelower
        global satlower
        global valuelower
        global hueupper
        global satupper
        global valueupper

        master = Tk()
        img = PhotoImage(file="hue.png")
        master.title("Value Sliders")

        def huevaluelow(val):
            huelow_q.put(int(val))
            #print("huelower changed to " + val)
        def satvaluelow(val):
            satlow_q.put(int(val))
        def valuevaluelow(val):
            valuelow_q.put(int(val))
        def huevalueup(val):
            hueup_q.put(int(val))
        def satvalueup(val):
            satup_q.put(int(val))
        def valuevalueup(val):
            valueup_q.put(int(val))
        def snapshot():
            snapshot_pass.put(1)

        huelowimg = Label(text = "Hue referance", image = img).pack()
        huelow = Scale(master, label = "Hue Lower", orient = HORIZONTAL, from_ = 0, to = 180, length = 500, command = huevaluelow).pack()
        satlow = Scale(master, label = "Saturation Lower", orient = HORIZONTAL, from_ = 0, to = 255, length = 500, command = satvaluelow).pack()
        valuelow = Scale(master, label = "Value Lower", orient = HORIZONTAL, from_ = 0, to = 255, length = 500, command = valuevaluelow).pack()

        hueup = Scale(master, label = "Hue Upper", orient = HORIZONTAL, from_ = 0, to = 180, length = 500, command = huevalueup).pack()
        satup = Scale(master, label = "Saturation Upper", orient = HORIZONTAL, from_ = 0, to = 255, length = 500, command = satvalueup).pack()
        valueup = Scale(master, label = "Value Upper", orient = HORIZONTAL, from_ = 0, to = 255, length = 500, command = valuevalueup).pack()
        btn_snapshot = Button(text = "Take Snapshot", command = snapshot).pack()

        master.mainloop()



class capture(Thread):
    """docstring for ClassName"""
    def __init__(self):
        super(capture, self).__init__()

    def run(self):
        global huelower
        global satlower
        global valuelower
        global hueupper
        global satupper
        global valueupper

        cap = cv2.VideoCapture(0)
        while True:
            _, frame = cap.read()

            if not huelow_q.empty():
                huelower = huelow_q.get()
            if not satlow_q.empty():
                satlower = satlow_q.get()
            if not valuelow_q.empty():
                valuelower = valuelow_q.get()
            if not hueup_q.empty():
                hueupper = hueup_q.get()
            if not satup_q.empty():
                satupper = satup_q.get()
            if not valueup_q.empty():
              valueupper = valueup_q.get()

            #print ("huelower recieved = " + str(huelower))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #hsv2color = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            lower_color = np.array([huelower, satlower, valuelower])
            upper_color = np.array([hueupper, satupper, valueupper])
            mask = cv2.inRange(hsv, lower_color, upper_color)

            extracted = cv2.bitwise_and(frame, frame, mask=mask)

            #cv2.imshow("Original", frame)
            #cv2.imshow("hsv", hsv)
            cv2.imshow("mask", mask)
            cv2.imshow("extracted", extracted)

            if not snapshot_pass.empty():
                snapshot_pass.get()
                cv2.imwrite("frame.png", extracted)

            k = cv2.waitKey(5) & 0xFF
            if k==27:
                break


        cv2.destroyAllWindows()
        cap.release()

gui_thread = gui()
capture_thread = capture()

gui_thread.start()
capture_thread.start()
# gui_thread.join()
# capture_thread.join()











