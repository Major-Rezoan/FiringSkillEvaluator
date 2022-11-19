import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity

def ssi_processing(scanned_image_before, scanned_image_after):
    gp_images = []
    ssi_masks = []

    def find_similarity(imgNo):
        before = scanned_image_before[imgNo]
        after = scanned_image_after[imgNo]
        before = cv2.resize(before, (800, 800))
        after = cv2.resize(after, (800, 800))

        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

        (score, diff) = structural_similarity(before_gray, after_gray, full=True)

        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = np.zeros(before.shape, dtype='uint8')
        filled_after = after.copy()
        thresh_copy = np.ones(before.shape, dtype='uint8')

        for c in contours:
            area = cv2.contourArea(c)
            if area > 10:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(before, (x, y), (x + w, y + h), (36,12,255), 2)
                cv2.drawContours(mask, [c], 0, (0,255,0), -1)
                cv2.drawContours(filled_after, [c], 0, (0,0,255), -1)
                cv2.drawContours(thresh_copy, [c], 0, (255,255,255), -1)

        invert_img = cv2.bitwise_not(thresh_copy)

        gp_images.append(after)
        ssi_masks.append(invert_img)

    for i in range(0,len(scanned_image_before)):
        find_similarity(i)
    return gp_images, ssi_masks

