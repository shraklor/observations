import cv2
import numpy as np
import urllib2
import abc


class Camera(object):
    def __init__(self):
        pass

    @abc.abstractMethod
    def read(self):
        pass

    def save(self, filename):
        image = self.read()
        cv2.imwrite(image, filename)

    def create(configuration):
        camera = None

        address = configuration['address']
        user = configuration['user']
        pwd = configuration['password']

        if configuration['type'] == 'ip':
            camera = IpCamera(address, user, pwd)
        elif configuration['type'] == 'usb':
            camera = UsbCamera(address)
        elif configuration['type'] == 'stream':
            camera = StreamCamera(address)

        return camera


class IpCamera(Camera):

    def __init__(self, address, user, password):
        pmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        pmgr.add_password(None, address, user, password)
        handler = urllib2.HTTPBasicAuthHandler(pmgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        self.url = address

    def read(self):
        stream = urllib2.urlopen(self.url)
        data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)


class UsbCamera(Camera):

    def __init__(self, number):
        self.capture = cv2.VideoCapture(number)

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
