import camera
import config
import cv2

class DetectorTypes(object):
    Face = 0
    Eyes = 1
    Mouth = 2
    Body = 3
    Licence = 4

    def __init__(self):
        pass

# end class



class Detector(object):

    # create haarcascades!

    def __init__(self, camera):
        self.camera = camera
        pass

    def detect(self, type=DetectorTypes.Face):
        frame = camera.read()
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if


        # look for faces
        faces = FaceRecognitionManager.faceCascade.detectMultiScale(grayImage, 1.3, 5)

        for (x, y, w, h) in faces:
            hasEyes = False
            hasMouth = False
            image = frame[y:y + h, x:x + w]

            # draw rectangle around entire face
            # cv2.rectangle( frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            grayFace = grayImage[y:y + h, x:x + w]

            # look for eyes
            eyes = FaceRecognitionManager.eyesCascade.detectMultiScale(grayFace)

            for (ex, ey, ew, eh) in eyes:
                hasEyes = True
                # draw rectangle around eyes
                # cv2.rectangle(faceColor, (ex, ey), (ex+ew, ey+eh), (0, 255, 255), 2)

            # look for mouth
            mouths = FaceRecognitionManager.smileCascade.detectMultiScale(grayFace)

            for (ex, ey, ew, eh) in mouths:
                hasMouth = True
                # draw rectangle around mouth
                # cv2.rectangle(faceColor, (ex, ey), (ex+ew, ey+eh), (255, 0, 255), 2)

            if ((hasEyes == True) and (hasMouth == True)):
                self.detected.append(image)

        return self.detected

    # this should be running in it's own thread
    def __motion(self):
        pass


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

    if c.pass:
        cam.password = c.password

    return Detector(cam)




if __name__ == '__main__':
    pass

# endif
