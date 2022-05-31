"""chỉ là file test thôi mà"""

from threading import Thread
from queue import Queue



class FileVideoStream:
    def __init__(self, path, queueSize=128):
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)
def start(self):
    t = Thread(target=self.updata, args=())
    t.daemon=True
    t.start()
    return self
def updata(self):
    while True:
        if self.stopped:
            return
        if not self.Q.full():
            (grabbed, frame)=self.stream.read()
            if not grabbed:
                self.stop()
                return
            self.Q.put(frame)
def read(self):
    return self.Q.get()
def more(self):
    return self.Q.qsize() > 0
def stop(self):
    self.stopped = True
from  imutils.video import FileVideoStream
from  imutils.video import FPS
import  numpy as np
import  argparse
import  imutils
import  time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
                help="path to input video file")
args = vars(ap.parse_args())
print("[INFO] starting video file thread...")
fvs= FileVideoStream(args["video"]).start()
time.sleep()
fps= FPS().start()
while fvs.more():
    frame = fvs.read()
    frame = imutils.resize(frame,width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])

    cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
    fps.update()

    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    fvs.stop()