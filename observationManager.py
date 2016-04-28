import detector
import recognizer
import config


if __name__ == '__main__':
    cameraInUse = config.Object()
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
