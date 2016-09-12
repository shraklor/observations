from event import Event
import cv2
import os


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
        self.continueDetecting = False
        self.isActive = False
        self._lastFrame = None
        self.camera = None
        self.FaceDetected = None
        self.MotionDetected = None

    @staticmethod
    def create(configuration, camera):
        response = Detector(configuration)
        response.camera = camera
        response.camera.FrameCaptured += response.OnFrameCaptured
        response.FaceDetected = Event()
        response.MotionDetected = Event()

        return response

    def OnFrameCaptured(self, frame):
        if self._lastFrame is None:
            self._lastFrame = frame

        print 'Frame Was Captured!'
        self.FaceDetected(frame)

        self._lastFrame = frame

    def detectMotion(self):
        pass

    def detectFaces(self, image):
        pass

    def detect(self, fps, area):
        self.continueDetecting = True
        self.isActive = True

        window = 'Image From {0}'.format(self.camera.name)
        cv2.namedWindow(window)

        print 'FPS: {0}, Area: {1}'.format(fps, area)
        while self.continueDetecting is True:
            frame = self.camera.read()
            x = area[0]
            y = area[1]
            w = area[2]
            h = area[3]
            ########### next 3 lines not needed
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
            cv2.imshow(window, frame)
            cv2.waitKey(1)
            ###########

            image = frame[y:y + h, x:x + w]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.FACE_CASCADE.detectMultiScale(gray, self._scaleFactor, self._minNeighbors)

            for (fx, fy, fw, fh) in faces:
                print 'face!'
                face = gray[y:fy + fh, x:fx + fw]
                eyes = self.EYES_CASCADE.detectMultiScale(face)
                glasses = self.GLASSES_CASCADE.detectMultiScale(face)

                if len(eyes) is 0 and len(glasses) is 0:
                    print 'no eyes/glasses'
                    continue

                print 'eyes/glasses'
                mouths = self.SMILE_CASCADE.detectMultiScale(face)
                if len(mouths) is 0:
                    print 'no mouth'
                    continue

                print 'must be a face!'
                self.FaceDetected(self.camera.name, fx, fy, fw, fh)

        cv2.destroyWindow(window)

    def detectO(self, fps, area):
        detected = {}

        frame = camera.read()
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = Detector.faceCascade.detectMultiScale(grayImage, config.detect.scaleFactor, config.detect.minNeighbors)

        for (x, y, w, h) in faces:
            detected.faces.append = (x, y, w, h)
        # endif requireFace

        eyes = Detector.eyesCascade.detectMultiScale(grayImage)

        for (ex, ey, ew, eh) in eyes:
            detected.eyes.append = (ex, ey, ew, eh)
        # endif requireEyes

        mouths = Detector.smileCascade.detectMultiScale(grayImage)

        for (ex, ey, ew, eh) in mouths:
            detected.mouths.append = (ex, ey, ew, eh)
        # endif requireMouth

        bodies = Detector.bodyCascade.detectMultiScale(grayImage)

        for (x, y, w, h) in bodies:
            detected.bodies.append = (x, y, w, h)
        # endif requireBody

        licences = Detector.licenceCascade.detectMultiScale(grayImage)

        for (x, y, w, h) in licences:
            detected.licences.append = (x, y, w, h)
        # endif requireBody

        return detected


# http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# https://blog.cedric.ws/opencv-simple-motion-detection
class MotionDetector(object):

    def __init__(self, camera):
        self.camera = camera
        self.running = False

    def start(self):    # this should launch separate thread that handles processing
        self.running = True

        firstFrame = None
        while True:
            frame = self.camera.read()
            frame = cv2.resize(frame, config.motion.resize, interpolation=cv2.INTER_LANCZOS4)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, config.motion.blur, 0)

            if firstFrame is None:
                firstFrame = gray
                continue

            frameDelta = cv2.absdiff(firstFrame, gray)
            threshold = cv2.threshold(frameDelta, config.motion.threshold, config.motion.max, cv2.THRESH_BINARY)[1]

            threshold = cv2.dilate(threshold, None, None, None, config.motion.dilateIterations)
            (contours, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL)

            for contour in contours:
                if cv2.contourArea(contour) < config.motion.minSize:
                    continue

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)


            if self.running is False:
                break

    def stop(self):
        self.running = False



def create(camera):
    c = config.cameras[camera]
    type = c.type
    address = c.address
    cam = type(address)

    if c.user:
        cam.user = c.user

    if len(c.password) > 0:
        cam.password = c.password

    return Detector(cam)




if __name__ == '__main__':
    pass

# endif
