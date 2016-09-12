from configobj import ConfigObj, flatten_errors
import validate
from detector import Detector
from camera import Camera
import cv2
from time import time, sleep
import threading

if __name__ == '__main__':
    config = ConfigObj('.\\config.cnf', configspec='.\\config.spec')
    validator = validate.Validator()
    results = config.validate(validator, preserve_errors=True)

    for entry in flatten_errors(config, results):
        [section, key, error] = entry
        if error == False:
            print 'in section "{0}" failed to find key "{1}"'.format(section, key)

    if key is not None:
        if (isinstance(error, validate.VdtValueError)):
            optionString = config.configspec[key]
            print 'key {0} was set to {1}'.format(key, config[key])
            print 'allowed value is: {0}'.format(optionString)

    # detector = Detector(config)
    counter = 0

    def OnFaceDetection(camera, x, y, w, h):
        print '{0} detected a face'.format(camera)





    # DETECTOR           DETECTOR              DETECTOR

    threads = {}

    for key in config['detectors']:
        cameraName = config['detectors'][key]['camera']

        if cameraName not in config['cameras']:
            raise KeyError('Failed to find "{0}" in camera listing for detection'.format(cameraName))

        camera = Camera.create(config, cameraName)
        detector = Detector.create(config, camera)
        threads['detector_'.format(cameraName)] = detector

        detector.FaceDetected += OnFaceDetection

        fps = config['detectors'][key]['fps']
        area = (config['detectors'][key]['area.x'], config['detectors'][key]['area.y'], config['detectors'][key]['area.h'], config['detectors'][key]['area.w'])
        print 'Creating detector for {0}'.format(cameraName)
        thread = threading.Thread(target=detector.detect, args=(fps, area))
        thread.daemon = True
        thread.start()

        # detector.spawn(camera, fps, area)
        # fps
        # area.x, y, h, w
        # cron.second, minute, hour, dow, day, month
        # type



        # if camera is not None:
        #     image = camera.read()
        #     cv2.namedWindow('dst_rt')
        #     cv2.imshow('dst_rt', image)
        #     cv2.waitKey(2000)
        #     cv2.destroyAllWindows()

    # detect.detectMotion()



    counter = 0

    # create camera and display image
    cam = None
    # cam = Camera.create(config, 'logitech')
    # cam = Camera.create(config, 'laptop')
    # cam = Camera.create(config, 'garage door')
    # cam = Camera.create(config, 'front door')
    # cam = Camera.create(config, 'backyard')

    # cam.FrameCaptured += OnFrameCaptured
    # if cam is not None:
    #    thread = threading.Thread(target=cam.stream, args=(5,))
    #    thread.daemon = True
    #    thread.start()
    #    cv2.namedWindow('dst_rt')
    #    image = cam.read()
    #    cv2.imshow('dst_rt', image)
    #    cv2.waitKey(2000)
    #    cv2.destroyAllWindows()

    while counter <= 25:
        sleep(1)
        counter += 1

        if counter > 15:
            for key in threads:
                # print type(threads[key])
                if isinstance(threads[key], Detector):
                    if threads[key].isActive is True:
                        print 'closing'
                        threads[key].continueDetecting = False


    # cam.FrameCaptured -= OnFrameCaptured
    # cv2.destroyAllWindows()

