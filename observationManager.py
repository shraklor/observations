import detector
import recognizer
import config


if __name__ == '__main__':
    cameraInUse = []
    # use the config info to do the needed work
    for camera in config.motion.cameras:
        if cameraInUse[camera.camera] is not None:
            Exception("Camera \"{0}\" is already in use".format(camera.camera))

        cameraInUse.append(camera.camera)
        print "Motion: Name{0}, Interval: {1}, MinArea: {2}\n".format(camera.camera, camera.interval, camera.minArea)
        camera = config.cameras[camera.camera]
        print camera
        print "----------------------\n"

    for watcher in config.detectors:
        if cameraInUse[watcher.camera] is not None:
            Exception("Camera \"{0}\" is already in use".format(watcher.camera))

        cameraInUse.append(watcher.camera)
        print "Watchers: Name: {0}, Area: {1}, Cron: {2}, IsActive: {3}".format(watcher.camera, watcher.area, watcher.cron, watcher.active)
        camera = config.cameras[watcher.camera]
        print camera
        print "----------------------\n"


# endif
