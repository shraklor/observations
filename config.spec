[haars]
path = string
eyes = string
glasses = string
face = string
mouth = string
body = string
licence = string

[debug]
border.color.face.r = integer(min=0,max=255)
border.color.face.g = integer(min=0,max=255)
border.color.face.b = integer(min=0,max=255)
border.color.eye.r = integer(min=0,max=255)
border.color.eye.g = integer(min=0,max=255)
border.color.eye.b = integer(min=0,max=255)
border.color.mouth.r = integer(min=0,max=255)
border.color.mouth.g = integer(min=0,max=255)
border.color.mouth.b = integer(min=0,max=255)
border.thickness = integer(min=0,max=5)

[detect]
scaleFactor = float
minNeighbors = integer
min.face.h = integer
min.face.w = integer
max.face.h = integer
max.face.w = integer
minConfidence = float

[detectors]
    [[__many__]]
    camera = string
    fps = integer(min=1, max=30)
    area.x = integer
    area.y = integer
    area.h = integer
    area.w = integer
    cron.second = integer(min=0,max=59)
    cron.minute = integer(min=0,max=59)
    cron.hour = integer(min=0,max=23)
    cron.dow = integer(min=0,max=6)
    cron.day = integer(min=0,max=31)
    cron.month = integer(min=0,max=11)
    active = boolean
    type = boolean

[recognizer]
auto_train = boolean
unknown = string
resize.h = integer(min=30)
resize.w = integer(min=40)

[training]
location = string
camera = string
delay = integer
count = integer


[motion]
resize.h = integer
resize.w = integer
blur.h = integer(min=1)
blur.w = integer(min=1)
threshold = integer
max = integer
dilateIterations = integer

    # this should be for each camera configured to motion
    [[cameras]]
        [[[__many__]]]
        interval = floats
        camera = string
        type = string
        [[[[areas]]]]
            [[[[[__many__]]]]]
            x = integer
            y = integer
            w = integer
            h = integer

        [[[[notification]]]]
            email = string
            subject = string
            phone = string
            message = string
            sound = string
            network = string


# list of cameras that can be used throughout all applications
[cameras]
    [[__many__]]
    name = string
    description = string
    type = string
    address = string
    user = string
    password = string
