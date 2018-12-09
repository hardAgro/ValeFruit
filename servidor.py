# USAGE
# python watershed.py --image images/coins_01.png

# import the necessary packages
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import cv2
from bottle import route, run
from bottle import static_file
import datetime

#VARIÁVEIS GLOBAIS
VALE_CONTAGEM = 0 
VALE_ESTIMATIVA = 0

def detectarUvas(mostrarJanela=False):
    global VALE_CONTAGEM 
    global VALE_ESTIMATIVA
    nonzero = 0

    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #     help="path to input image")
    # args = vars(ap.parse_args())

    # load the image and perform pyramid mean shift filtering
    # to aid the thresholding step

    # Se a imagem for fixa
    # path = args["image"]
    path = "img/blob7.jpg"

#     image = cv2.imread(path)
    # Para a imagem da camera do computador para fins de simulação
    cam = cv2.VideoCapture(0)
    ret, image = cam.read()

    image = 255-image
    shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
    # cv2.imshow("Input", image)
    # cv2.imshow("Shifted", shifted)

    # convert the mean shift image to grayscale, then apply
    # Otsu's thresholding
    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    nonzero = cv2.countNonZero(thresh)
    print("NON-ZERO THRESH: ", nonzero)
    # cv2.imshow("Thresh", thresh)

    # compute the exact Euclidean distance from every binary
    # pixel to the nearest zero pixel, then find peaks in this
    # distance map
    D = ndimage.distance_transform_edt(thresh)
    localMax = peak_local_max(D, indices=False, min_distance=20,
        labels=thresh)

    # perform a connected component analysis on the local peaks,
    # using 8-connectivity, then appy the Watershed algorithm
    markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
    labels = watershed(-D, markers, mask=thresh)
    # print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))
    print("[INFO] Segmentos: {}".format(len(np.unique(labels)) - 1))


    # loop over the unique labels returned by the Watershed
    # algorithm 
    cont = 0
    for label in np.unique(labels):
        # if the label is zero, we are examining the 'background'
        # so simply ignore it
        if label == 0:
            continue

        # otherwise, allocate memory for the label region and draw
        # it on the mask
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[labels == label] = 255

        # detect contours in the mask and grab the largest one
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        c = max(cnts, key=cv2.contourArea)
        # draw a circle enclosing the object
        ((x, y), r) = cv2.minEnclosingCircle(c)

        # print("#{}".format(label), r)
        if r > 50 and r < 100:
            cont+=1
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
    #     cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
    #         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    VALE_CONTAGEM = cont
    print("[INFO] Contagem: ", VALE_CONTAGEM)
    # Estimativa feita a partir do ajuste de reta feita com os testes realizados
    # N uvas	
    # 63	blob5
    # 58	blob6
    # 68	blob7
    # 25	blob8
    # 31	blob9
    # 16	blob10
    VALE_ESTIMATIVA = (nonzero - 167776.37)/7923.75
    if VALE_ESTIMATIVA < 0:
        VALE_ESTIMATIVA = 0
    print("[INFO] Estimativa: ", VALE_ESTIMATIVA)
    # show the output image
    if mostrarJanela:
        cv2.imshow("Output", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
# detectarUvas()
# 21
# 63





@route('/hello')
def hello():
    return "Hello World!"
# distance to object (mm) = focal length (mm) * real height of the object (mm) * image height (pixels)
# do = fl * rho * ih
# rho = do/ (fl * ih)

@route('/valefruit')
def hello():
    global VALE_ESTIMATIVA
    global VALE_CONTAGEM
    detectarUvas()
    return '''<h2>ValeFruit-Data</h2>
                <div>contagem: {} <br/></div>
                <div>estimativa: {} <br/></div>
                <div>datetime: {} <br/></div>
                '''.format(VALE_CONTAGEM, VALE_ESTIMATIVA, datetime.datetime.now())

@route('/valefruitestimativa')
def hello():
    global VALE_ESTIMATIVA
    global VALE_CONTAGEM
    detectarUvas()
    return '''{}'''.format(VALE_ESTIMATIVA)

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/home/ruan/Documents/hackathon/static')

run(host='192.168.1.139', port=8080, debug=True)
