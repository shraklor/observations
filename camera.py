import cv2
import numpy as np
import urllib2


class Camera(object):
    def __init__(self):
        pass

    # @abstractMethod
    def read(self):
        pass

    def save(self, filename):
        image = self.read()
        cv2.imwrite(image, filename)


class IpCamera(Camera):

    def __init__(self, config):
        pmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        pmgr.add_password(None, config.address, config.user, config.password)
        handler = urllib2.HTTPBasicAuthHandler(pmgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        self.url = config.address

    def read(self):
        stream = urllib2.urlopen(self.url)
        data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)


class LocalCamera(Camera):

    def __init__(self, config):
        self.capture = cv2.VideoCapture(config.address)

    def read(self):
        image = None
        if self.capture.isOpened():
            _, image = self.capture.read()

        return image


class StreamCamera(Camera):

    def __init__(self, config):
        self.stream = config.address

    def read(self):
        data = self.stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)
