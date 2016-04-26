

general = {}
general.haars = {}
general.haars.path = '.\\haarcascades'
general.haars.eyes = 'haarcascade_eye_tree_eyeglasses.xml'
general.haars.face = 'haarcascade_frontalface_default.xml'
general.haars.mouth = 'haarcascade_smile.xml'
general.haars.body = 'haarcascade_upperbody.xml'
general.haars.other = 'haarcascade_licence_plate_rus_16stages.xml'
general.debug = {}
general.debug.FACE_BORDER_COLOR = (255, 0, 0)
general.debug.EYE_BORDER_COLOR = (0, 255, 0)
general.debug.MOUTH_BORDER_COLOR = (255, 255, 0)
general.debug.BORDER_THICKNESS = 2



# for use in the detector application
detect = {}
detect.scaleFactor = 1.3
detect.minNeighbors = 1.3
detect.minFaceSize = (30, 30)
detect.maxFaceSize = (70, 70)
detect.minConfidence = .75


# for use in the face recognizer application
recognizer = {}
recognizer.auto_train = True
recognizer.unknown = 'unknown'
recognizer.resize = (92, 115)


# for use in the motion detection application
watchers = []
watchers[0].camera = 'front door'
watchers[0].area = (x,y,h,w)
watchers[0].cron = (s,m,h,dow,dom,mon)
watchers[0].active = False

watchers[1].camera = 'kitchen'
watchers[1].area = (x,y,h,w)
watchers[1].cron = (s,m,h,dow,dom,mon)
watchers[1].active = False


# for use in the trainer
training = {}
training.location = '.\\training'
training.camera = ''
training.delay = 5
training.count = 30


motion = {}
motion.resize = (500, 500)
motion.blur = (21, 21)
motion.threshold = 25
motion.max = 255
motion.dilateIterations = 2

# this should be for each camera configured to motion
motion.interval = .25
motion.minArea = 500


# list of cameras that can be used throughout all applications
cameras = []
cameras['office'] = {}
cameras['office'].name = 'office'
cameras['office'].type = 'usb'
cameras['office'].address = '0'

cameras['front door'] = {}
cameras['front door'].name = 'front door'
cameras['front door'].type = 'ip'
cameras['front door'].address = 'http://192.168.111.164'
cameras['front door'].user = ''
cameras['front door'].password = ''

cameras['kitchen'] = {}
cameras['kitchen'].name = 'kitchen'
cameras['kitchen'].type = 'ip'
cameras['kitchen'].address = '192.168.111.163'
cameras['kitchen'].user = ''
cameras['kitchen'].password = ''


