from configobj import ConfigObj


if __name__ == '__main__':
    config = ConfigObj('.\\config.cnf')

    haars = config['general']['haars']

    print "in [haars] section"
    for val in haars:
        print "\tkey: {0} => value {1}".format(val, haars[val])

    motion = config['motion']
    print "in [motion] section"
    print "\tresize => {0}".format(motion['resize'])
    print "\tblur   => {0}".format(motion['blur'])
    print "\tthreshold => {0}".format(motion['threshold'])
    print "\tmax => {0}".format(motion['max'])
    print "\tdilateIterations => {0}".format(motion['dilateIterations'])

    cameras = motion['cameras']
    print "\tin [motion][cameras] section"
    for val in cameras:
        print "\t\tkey: {0} => value {1}".format(val, cameras[val])

    # print motion
    exit()

    cameraInUse = {}
    # use the config info to do the needed work
    for camera in config.motion.cameras:
        print "Motion=> Name: {0}, Interval: {1}, MinArea: {2}\n".format(camera.camera, camera.interval, camera.minArea)
        cam = None
        for c in config.cameras:
            if c.name == camera.camera:
                cam = c
                break

        print dir(cam)
        print "----------------------\n"

    for watcher in config.detectors:
        print "Watchers: Name: {0}, Area: {1}, Cron: {2}, IsActive: {3}".format(watcher.camera, watcher.area, watcher.cron, watcher.active)
        cam = None
        for c in config.cameras:
            if c.name == watcher.camera:
                cam = c
                break

        print dir(cam)
        print "----------------------\n"


# endif
