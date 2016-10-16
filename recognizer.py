import cv2
import time
import uuid
import os
import event


class Recognizer(object):

    def __init__(self, configuration):
        pass

    def recognize(self, face):
        pass

# end class


class Trainer(object):

    def __init__(self, recognizer, path='.\\training'):
        self.path = path
        self.recognizer = recognizer
        self.loaded = False

    def add(self, name, image):
        path = '{0}\\{0}'.format(self.path, name)
        filename = '{0}\\{1}.png'.format(path, uuid.uuid4())

        if os.path.exists(path) is False:
            os.makedirs(path)

        image = cv2.resize(image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        cv2.imwrite(filename, gray)
        self.loaded = False

    def run(self, name, delay=5, count=5):
        counter = 0

        while counter < count:
            faces = self.recognizer.detect()

            if len(faces) == 1:
                self.add(name, faces[0])

            time.sleep(delay)
            counter += 1

    def load(self):
        self.loaded = False
        images = []
        labels = []
        counter = 0

        if os.path.exists(self.path) is False:
            os.makedirs(self.path)

        for d in os.listdir(self.path):
            dir = os.path.join(self.path, d)

            if os.path.isfile(dir):
                continue

            for f in os.listdir(dir):
                file = os.path.join(dir, f)

                if os.path.isdir(file):
                    continue

                image = cv2.imread(file)
                images.append(image)
                labels.append(d)
                counter += 1

        self.loaded = True

        return images, labels

# end class


if __name__ == '__main__':
    pass

# endif
