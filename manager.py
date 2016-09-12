from configobj import ConfigObj, flatten_errors
import validate
import detector

if __name__ == '__main__':
    config = ConfigObj('.\\config.cnf', configspec='.\\config.spec')
    validator = validate.Validator()
    results = config.validate(validator, preserve_errors=True)

    for entry in flatten_errors(config, results):
        [section, key, error] = entry
        if error is False:
            print 'in section "{0}" failed to find key "{1}"'.format(section, key)

    detect = detector.Detector(config)


    detect.detectMotion()

# endif
