import cv2
import numpy as np
import uuid
import os
import sys

sys.path.append('c:\python2.7\site-packages')

class FaceRecognitionManager(object):
    faceCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_frontalface_default.xml')
    eyesCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_eye_tree_eyeglasses.xml')
    # eyesCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_eye.xml')
    smileCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_smile.xml')
    FACE_WIDTH = 92
    FACE_HEIGHT = 112

    def __init__(self):
        self.trainingPath = '.\\training'
        self.images = []
        self.labels = []
        self.names = []
        self.model = cv2.face.createEigenFaceRecognizer()
        # self.model = cv2.face.createFisherFaceRecognizer()
        # self.model = cv2.face.createLBPHFaceRecognizer()
        self.reload()

    def reload(self):
        images = []
        labels = []
        names = []

        counter = 0

        if os.path.exists(self.trainingPath) is False:
            os.makedirs(self.trainingPath)

        for d in os.listdir(self.trainingPath):
            dir = os.path.join(self.trainingPath, d)

            if os.path.isfile(dir):
                continue

            for f in os.listdir(dir):
                file = os.path.join(dir, f)

                if os.path.isdir(file):
                    continue

                image = cv2.imread(file)
                images.append(image)
                labels.append(1)
                names.append(d)
                counter += 1

        if counter > 0:
            self.model.train(np.asarray(images), np.asarray(labels))

    def __add(self, name, face):
        personPath = '{0}\\{0}'.format(self.trainingPath, name)
        filename = '{0}\\{1}.png'.format(personPath, uuid.uuid4())

        if os.path.exists(personPath) is False:
            os.makedirs(personPath)

        face = cv2.resize(face, (FaceRecognitionManager.FACE_WIDTH, FaceRecognitionManager.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        cv2.imwrite(filename, gray)
        self.reload()

    def detect(self):
        self.detected = []

        capture = cv2.VideoCapture(1)
        result, frame = capture.read()
        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # look for faces
        faces = FaceRecognitionManager.faceCascade.detectMultiScale(grayImage, 1.3, 5)

        for (x, y, w, h) in faces:
            hasEyes = False
            hasMouth = False
            image = frame[y:y+h, x:x+w]

            # draw rectangle around entire face
            # cv2.rectangle( frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            grayFace = grayImage[y:y+h, x:x+w]

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

            if (( hasEyes == True ) and ( hasMouth == True )):
                self.detected.append(image)

        return self.detected

    def recognize(self, face):
        face = cv2.resize(face, (FaceRecognitionManager.FACE_WIDTH, FaceRecognitionManager.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        name = 'unknown'

        try:
            predicted, conf = self.model.predict(gray)
            print 'predicted {0} with a confidence of {1}'.format(predicted, conf)
            name = 'brad'
        except:
            pass

        return name

    def run(self, callback):
        self.detect()

        for face in self.detected:
            name = self.recognize(face)

            if name is 'unknown':
                self.__add(name, face)
            else:
                callback(name, face)


def my_callback(name, face):
    title = 'This is the face of [{0}]'.format(name)
    cv2.imshow(title, face)
    print title

if __name__ == '__main__':

    facer = FaceRecognitionManager()

    while True:
        facer.run(my_callback)
        key = cv2.waitKey(20)

        if key == 27:
            break

    cv2.destroyAllWindows()

# endif
