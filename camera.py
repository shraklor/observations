import cv2
import numpy as np
import urllib2


class Camera(object):
    def __init__(self):
        pass

    @abstractMethod
    def read(self):
        pass

    def save(self, filename):
        image = self.read()
        cv2.imwrite(image, filename)


class IpCamera(Camera):

    def __init__(self, url, user=None, password=None):
        pmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        pmgr.add_password(None, url, user, password)
        handler = urllib2.HTTPBasicAuthHandler(pmgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        self.url = url

    def read(self):
        stream = urllib2.urlopen(self.url)
        data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)


class LocalCamera(Camera):

    def __init__(self, camera=0):
        self.capture = cv2.VideoCapture(camera)

    def read(self):
        image = None
        if self.capture.isOpened():
            _, image = self.capture.read()

        return image


class StreamCamera(Camera):

    def __init__(self, stream):
        self.stream = stream

    def read(self):
        data = self.stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)
