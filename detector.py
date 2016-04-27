import camera
import config
import cv2
import os

class DetectorTypes(object):
    Unspecified = 0
    Face = 1
    Eyes = 2
    Mouth = 4
    Body = 8
    Licence = 16

    def __init__(self):
        pass

# end class


class Detector(object):
    # create haarcascades!
    faceCascade = cv2.CascadeClassifier(os.path.join( config.general.haars.path, config.general.haars.face))
    eyesCascade = cv2.CascadeClassifier(os.path.join( config.general.haars.path, config.general.haars.eyes))
    smileCascade = cv2.CascadeClassifier(os.path.join( config.general.haars.path, config.general.haars.mouth))
    bodyCascade = cv2.CascadeClassifier(os.path.join( config.general.haars.path, config.general.haars.body))
    licenceCascade = cv2.CascadeClassifier(os.path.join( config.general.haars.path, config.general.haars.licence))

    def __init__(self, camera):
        self.camera = camera
        pass

    def detect(self, type=DetectorTypes.Face):
        detected = {}
        requireFace = False
        requireEyes = False
        requireMouth = False
        requireBody = False
        requireLicence = False
        requiredCount = 0
        foundCount = 0

        frame = camera.read()
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if ( type & DetectorTypes.Face ) == DetectorTypes.Face:
            requiredCount += 1
            requireFace = True

        if (type & DetectorTypes.Eyes) == DetectorTypes.Eyes:
            requiredCount += 1
            requireEyes = True

        if (type & DetectorTypes.Mouth) == DetectorTypes.Mouth:
            requiredCount += 1
            requireMouth = True

        if (type & DetectorTypes.Mouth) == DetectorTypes.Mouth:
            requiredCount += 1
            requireBody = True

        if (type & DetectorTypes.Mouth) == DetectorTypes.Mouth:
            requiredCount += 1
            requireLicence = True


        if requireFace is True:
            detected.faces = []
            faces = Detector.faceCascade.detectMultiScale(grayImage, config.detect.scaleFactor, config.detect.minNeighbors)

            if len(faces) > 0:
                foundCount += 1

            for (x, y, w, h) in faces:
                detected.faces.append = (x, y, w, h)
        # endif requireFace

        if requireEyes is True:
            detected.eyes = []
            eyes = Detector.eyesCascade.detectMultiScale(grayImage)

            if len(eyes) > 0:
                foundCount += 1

            for (ex, ey, ew, eh) in eyes:
                detected.eyes.append = (ex, ey, ew, eh)
        # endif requireEyes

        if requireMouth is True:
            detected.mouths = []
            mouths = Detector.smileCascade.detectMultiScale(grayImage)

            if len(mouths) > 0:
                foundCount += 1

            for (ex, ey, ew, eh) in mouths:
                detected.mouths.append = (ex, ey, ew, eh)
        # endif requireMouth

        if requireBody is True:
            detected.bodies = []
            bodies = Detector.bodyCascade.detectMultiScale(grayImage)

            if len(bodies) > 0:
                foundCount += 1

            for (x, y, w, h) in bodies:
                detected.bodies.append = (x, y, w, h)
        # endif requireBody

        if requireLicence is True:
            detected.licences = []
            licences = Detector.licenceCascade.detectMultiScale(grayImage)

            if len(licences) > 0:
                foundCount += 1

            for (x, y, w, h) in licences:
                detected.licences.append = (x, y, w, h)
        # endif requireBody

        response = False
        if requiredCount == foundCount:
            detected.image = frame
            response = True
        else:
            detected = {}

        return response, detected


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
