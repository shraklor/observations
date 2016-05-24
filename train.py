import cv2
import numpy as np
import uuid
import os
import sys
import time


class Trainer(object):
    faceCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_frontalface_default.xml')
    eyesCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_eye_tree_eyeglasses.xml')
    # eyesCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_eye.xml')
    smileCascade = cv2.CascadeClassifier('d:\data\haarcascade\haarcascade_smile.xml')
    FACE_WIDTH = 92
    FACE_HEIGHT = 112

    def __init__(self, configuration):
        self.loaded = False
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

        self.loaded = True

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


if __name__ == '__main__':
    pass
# endif
