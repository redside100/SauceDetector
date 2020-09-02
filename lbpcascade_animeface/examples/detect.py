from builtins import RuntimeError

import cv2
import numpy
import os.path


def detect(pil_image):
    cascade_file = os.path.abspath("./lbpcascade_animeface/lbpcascade_animeface.xml")
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    image = numpy.array(pil_image)
    cascade = cv2.CascadeClassifier(cascade_file)
    # image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))

    regions = []
    for (x, y, w, h) in faces:
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        regions.append((x, y, w, h))

    return regions


    # cv2.imshow("AnimeFaceDetect", image)
    # cv2.waitKey(0)
    # cv2.imwrite("out.png", image)


# if len(sys.argv) != 2:
#     sys.stderr.write("usage: detect.py <filename>\n")
#     sys.exit(-1)
    
# detect(sys.argv[1])
