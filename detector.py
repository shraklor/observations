from event import Event
import cv2
import os
from time import time, sleep


class Detector(object):

    def __init__(self, configuration):
        haars = configuration['haars']
        self.FACE_CASCADE = cv2.CascadeClassifier(os.path.join(haars['path'], haars['face']))
        self.EYES_CASCADE = cv2.CascadeClassifier(os.path.join(haars['path'], haars['eyes']))
        self.GLASSES_CASCADE = cv2.CascadeClassifier(os.path.join(haars['path'], haars['glasses']))
        self.SMILE_CASCADE = cv2.CascadeClassifier(os.path.join(haars['path'], haars['mouth']))
        self.BODY_CASCADE = cv2.CascadeClassifier(os.path.join(haars['path'], haars['body']))
        self.LICENCE_CASCADE = cv2.CascadeClassifier(os.path.join(haars['path'], haars['licence']))

        self._scaleFactor = configuration['detect']['scaleFactor']
        self._minNeighbors = configuration['detect']['minNeighbors']
        self._minFaceSize = (configuration['detect']['min.face.h'], configuration['detect']['min.face.w'])
        self._maxFaceSize = (configuration['detect']['max.face.h'], configuration['detect']['max.face.w'])
        self._minConfidence = configuration['detect']['minConfidence']

        self._resizeH = configuration['motion']['resize.h']
        self._resizeW = configuration['motion']['resize.w']
        self._blur = (configuration['motion']['blur.h'], configuration['motion']['blur.w'])
        self._threshold = configuration['motion']['threshold']
        self._max = configuration['motion']['max']
        self._dilateIterations = configuration['motion']['dilateIterations']

        self.motionDetecting = False
        self.motionIsActive = False
        self.facesDetecting = False
        self.facesIsActive = False
        self._lastFrame = None
        self.camera = None
        self.FaceDetected = None
        self.MotionDetected = None

    @staticmethod
    def create(configuration, camera):
        response = Detector(configuration)
        response.camera = camera
        response.FaceDetected = Event()
        response.MotionDetected = Event()

        return response

    def faces(self, fps, area):
        self.facesDetecting = True
        self.facesIsActive = True

        frameperiod = 1.0 / fps
        now = time()
        nextframe = now + frameperiod

        while self.facesDetecting is True:
            frame = self.camera.read()
            x = area[0]
            y = area[1]
            h = area[2]
            w = area[3]

            image = frame[y:y + h, x:x + w]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.FACE_CASCADE.detectMultiScale(gray, self._scaleFactor, self._minNeighbors)

            for (fx, fy, fw, fh) in faces:
                face = gray[y:fy + fh, x:fx + fw]
                eyes = self.EYES_CASCADE.detectMultiScale(face, 1.2, 4)

                if len(eyes) is not 2:
                    continue

                smiles = self.SMILE_CASCADE.detectMultiScale(face, 3.0, 6)

                if len(smiles) is 0:
                    continue

                # cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)

                # for (ex, ey, ew, eh) in eyes:
                #    cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                # for (mx, my, mw, mh) in smiles:
                #    cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (255, 255, 120), 2)

                self.FaceDetected(self.camera.name, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                break       # if we detect 1 face, it's good enough

            while now < nextframe:
                sleep(nextframe - now)
                now = time()
            nextframe += frameperiod

        self.facesIsActive = False

    # http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
    # https://blog.cedric.ws/opencv-simple-motion-detection
    def motion(self, delay, area, minArea):
        self.motionDetecting = True
        self.motionIsActive = True

        window = 'Motion Image From {0}'.format(self.camera.name)
        cv2.namedWindow(window)

        previous = None

        frameperiod = 1.0 / delay
        now = time()
        nextframe = now + frameperiod

        while self.motionDetecting is True:
            frame = self.camera.read()
            x = area[0]
            y = area[1]
            h = area[2]
            w = area[3]

            image = frame[y:y + h, x:x + w]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, self._blur, 0)

            if previous is None:
                previous = gray
                continue

            delta = cv2.absdiff(previous, gray)
            thresh = cv2.threshold(delta, self._threshold, self._max, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=self._dilateIterations)
            (_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                print contour
                if cv2.contourArea(contour) < minArea:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                self.MotionDetected(self.camera.name, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow(window, frame)

            while now < nextframe:
                sleep(nextframe - now)
                now = time()
            nextframe += frameperiod

        cv2.imshow(window, frame)
        cv2.waitKey(1)

        self.motionIsActive = False
        cv2.destroyAllWindows()


if __name__ == '__main__':
    pass

# endif
