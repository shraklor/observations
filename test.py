import cv2


while True:
    capture = cv2.VideoCapture(0)
    result, frame = capture.read()

    print 'results {0}'.format(result)
    if ( result is True ):
        cv2.imshow('testing', frame)

    key = cv2.waitKey(20)

    if key == 27:
        break

cv2.destroyAllWindows()

