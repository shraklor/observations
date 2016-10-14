import cv2
import numpy as np
import urllib2
import security
from event import Event
from time import time, sleep


class Camera(object):
    def __init__(self):
        self.FrameCaptured = Event()
        self.name = ''

    def read(self):
        raise NotImplementedError

    def save(self, filename):
        image = self.read()
        cv2.imwrite(image, filename)

    def stream(self, fps):
        frameperiod = 1.0 / fps
        now = time()
        nextframe = now + frameperiod
        name = 'image_{0}'.format(self.name)
        cv2.namedWindow(name)

        while len(self.FrameCaptured) > 0:
            frame = self.read()
            cv2.imshow(name, frame)
            cv2.waitKey(1)
            self.FrameCaptured(frame)

            while now < nextframe:
                sleep(nextframe - now)
                now = time()
            nextframe += frameperiod

        cv2.destroyWindow(name)

    @staticmethod
    def create(configuration, name):
        camera = None

        if 'cameras' not in configuration:
            raise KeyError('Failed to find cameras listing in configuration settings')

        if name not in configuration['cameras']:
            raise KeyError('Failed to find camera ["{0}"] in cameras listing'.format(name))

        config = configuration['cameras'][name]

        if 'type' in config:
            typ = config['type']
        else:
            raise KeyError('Failed to find "type" of camera in configuration settings for...well the camera')

        if 'address' in config:
            address = config['address']
        else:
            raise KeyError('Failed to find "address" of camera in configuration settings for...well the camera')

        if 'user' in config:
            user = config['user']
            if len(user) > 0:
                user = security.Security.decrypt(user)
        else:
            user = ''

        if 'password' in config:
            pwd = config['password']
            if len(pwd) > 0:
                pwd = security.Security.decrypt(pwd)
        else:
            pwd = ''

        if typ == 'ip':
            camera = IpCamera(name, address, user, pwd)
        elif typ == 'usb':
            camera = UsbCamera(name, address)
        elif typ == 'stream':
            camera = StreamCamera(name, address)

        return camera


class IpCamera(Camera):

    def __init__(self, name, address, user, password):
        Camera.__init__(self)
        self.name = name
        self.url = address.replace('{USER}', user).replace('{PASSWORD}', password)

    def read(self):
        capture = cv2.VideoCapture()
        capture.open(self.url)
        _, image = capture.read()

        return image


class UsbCamera(Camera):

    def __init__(self, name, number):
        Camera.__init__(self)
        self.name = name
        number = int(float(number))
        self.camera = number

    def read(self):
        image = None

        capture = cv2.VideoCapture(self.camera)

        if capture.isOpened():
            _, image = capture.read()

        return image


class StreamCamera(Camera):

    def __init__(self, name, stream):
        Camera.__init__(self)
        self.name = name
        self.stream = stream

    def read(self):
        data = self.stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)
