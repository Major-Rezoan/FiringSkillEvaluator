import cv2
import os
import numpy as np
from svm_error_detection import error_by_svm

def draw_polyline(img, points):
    pts = np.array([points], np.int32)
    arc = cv2.polylines(img, [pts], isClosed=False, color=(150, 150, 0), thickness=1)
    return arc

def draw_ellipse(img, center=None, axesLength=None, angle=0):
    window_name = 'Error Analysis'
    angle = 0
    startAngle = 0
    endAngle = 360
    color = (255, 40, 255)
    thickness = 2
    cv2.ellipse(img, center, axesLength, angle, startAngle, endAngle, color, thickness)
    cv2.rectangle(img, (10, 10), (20, 10), 255, cv2.FILLED)
    return img

def error_list(x_length, y_length, x1, x2, x3, group):
    if group > 11 and (x_length > 11 or y_length > 11):
        if x_length > 3*y_length:
            error_name='Long Horizontal Error'
        elif y_length > 3*x_length:
            error_name='Long Vertical Error'
        elif ((sum(x1)<150) and (x2**2) > ((x1[0])**2+(x1[1])**2+(x1[2])**2)):
            if (x2==x3):
                error_name = 'Impatient Shot'
            else:
                error_name = 'Bi-focal Error'
        else:
            error_name='Scattered Group'
    else:
        error_name='No Listed Error'
    return error_name


def directional_error(img, points, x1, x2, x3, group):
    X = np.array([x[0] for x in points])
    Y = np.array([x[1] for x in points])
    center=(int(np.mean(X)), int(np.mean(Y)))
    x_length=int(np.sqrt(X.var()))*2
    y_length=int(np.sqrt(Y.var()))*2

    error_name = error_list(x_length=x_length, y_length=y_length, x1=x1, x2=x2, x3=x3, group=group)

    if group > 11:
        error_name_svm = error_by_svm(points)
        if error_name == error_name_svm:
            error_name = error_name
        else:
            error_name = error_name + '/' + error_name_svm

    error_img = draw_ellipse(img, center, axesLength=(x_length,y_length))
    error_img = draw_polyline(error_img, points)


    return error_name, error_img

