class Object(object):
    pass

general = Object()
general.haars = Object()
general.haars.path = '.\\haarcascades'
general.haars.eyes = 'haarcascade_eye_tree_eyeglasses.xml'
general.haars.face = 'haarcascade_frontalface_default.xml'
general.haars.mouth = 'haarcascade_smile.xml'
general.haars.body = 'haarcascade_upperbody.xml'
general.haars.licence = 'haarcascade_licence_plate_rus_16stages.xml'
general.debug = Object()
general.debug.FACE_BORDER_COLOR = (255, 0, 0)
general.debug.EYE_BORDER_COLOR = (0, 255, 0)
general.debug.MOUTH_BORDER_COLOR = (255, 255, 0)
general.debug.BORDER_THICKNESS = 2


# for use in the detector application
detect = Object()
detect.scaleFactor = 1.3
detect.minNeighbors = 5
detect.minFaceSize = (30, 30)
detect.maxFaceSize = (70, 70)
detect.minConfidence = .75


# for use in the motion detection application
detectors = []
detectors.append(Object())
detectors[0].camera = 'front door'
detectors[0].area = (0, 0, 480, 760)
# detectors[0].cron = (s,m,h,dow,dom,mon)
detectors[0].cron = (0, 0, 0, 0, 0, 0)
detectors[0].active = False
detectors[0].type = False

detectors.append(Object())
detectors[1].camera = 'kitchen'
detectors[1].area = (0, 0, 480, 760)
# detectors[1].cron = (s,m,h,dow,dom,mon)
detectors[1].cron = (0, 0, 0, 0, 0, 0)
detectors[1].active = False


# for use in the face recognizer application
recognizer = Object()
recognizer.auto_train = True
recognizer.unknown = 'unknown'
recognizer.resize = (92, 115)


# for use in the trainer
training = Object()
training.location = '.\\training'
training.camera = ''
training.delay = 5
training.count = 30


motion = Object()
motion.resize = (500, 500)
motion.blur = (21, 21)
motion.threshold = 25
motion.max = 255
motion.dilateIterations = 2

# this should be for each camera configured to motion
motion.cameras = []
motion.cameras.append(Object())
motion.cameras[0].interval = .25
motion.cameras[0].minArea = 500
motion.cameras[0].camera = 'office'


# list of cameras that can be used throughout all applications
cameras = []
cameras.append(Object())
cameras[0] = Object()
cameras[0].name = 'office'
cameras[0].type = 'usb'
cameras[0].address = '0'

cameras.append(Object())
cameras[1] = Object()
cameras[1].name = 'front door'
cameras[1].type = 'ip'
cameras[1].address = 'http://192.168.111.164'
cameras[1].user = ''
cameras[1].password = ''

cameras.append(Object())
cameras[2] = Object()
cameras[2].name = 'kitchen'
cameras[2].type = 'ip'
cameras[2].address = '192.168.111.163'
cameras[2].user = ''
cameras[2].password = ''


