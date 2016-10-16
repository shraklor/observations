from configobj import ConfigObj, flatten_errors
import validate
from detector import Detector
from recognizer import Recognizer
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
    sentEmail = False

    def OnMotionDetection(camera, image):
        print '{0} detected motion'.format(camera)


    def OnFaceDetection(camera, image):
        print '{0} detected a face'.format(camera)

        global sentEmail
        if sentEmail is False:
            import gmailer
            import tempfile
            import os
            # save image to temp file
            # pass temp file to emailer
            fp = tempfile.NamedTemporaryFile()
            filename = '{0}.jpeg'.format(fp.name)
            fp.close()
            print 'saving {0}'.format(filename)

            cv2.imwrite(filename, image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            sentEmail = True

            # message = dict()
            # message['to'] = 'brad.vanselous@gmail.com'
            # message['subject'] = 'Image From {0}'.format(camera)
            # message['body'] = 'Here is the body of the message!!'
            # message['attachment'] = filename

            mailer = gmailer.GMailer(config)
            mailer.send(config['detectors'][camera]['notification'], camera, filename)
            # email('{0} detected a face'.format(camera), 'brad.vanselous@gmail.com', filename)

            os.unlink(filename)


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
        thread = threading.Thread(target=detector.faces, args=(fps, area))
        thread.daemon = True
        thread.start()

    for key in config['motion']:
        cameraName = config['motion'][key]['camera']

        if cameraName not in config['cameras']:
            raise KeyError('Failed to find "{0}" in camera listing for detection'.format(cameraName))

        camera = Camera.create(config, cameraName)
        detector = Detector.create(config, camera)
        threads['detector_'.format(cameraName)] = detector

        detector.MotionDetected += OnMotionDetection

        fps = config['motion'][key]['fps']
        area = (config['motion'][key]['area.x'], config['detectors'][key]['area.y'], config['detectors'][key]['area.h'], config['detectors'][key]['area.w'])
        print 'Creating motion for {0}'.format(cameraName)
        thread = threading.Thread(target=detector.motion, args=(fps, area, 500))
        thread.daemon = True
        thread.start()



    counter = 0
    MAX_COUNTS = 20
    while counter <= MAX_COUNTS:
        sleep(1)
        counter += 1

        if counter > (MAX_COUNTS - 5):
            for key in threads:
                # print type(threads[key])
                if isinstance(threads[key], Detector):
                    if threads[key].motionIsActive is True:
                        print 'closing motion capture'
                        threads[key].motionDetecting = False
                    if threads[key].facesIsActive is True:
                        print 'closing face detection'
                        threads[key].facesDetecting = False


                            # cam.FrameCaptured -= OnFrameCaptured
    # cv2.destroyAllWindows()

