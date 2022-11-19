import numpy as np
import cv2

def scan_and_preprocess(all_paths):
    path = "data_from_scan"
    cleaned_image_before = []
    cleaned_image_after = []

    def scan_and_crop(counter):
        if counter < 4:
            readpath = all_paths[counter]
            readpath_2 = all_paths[counter+4]
        else:
            readpath = all_paths[counter+4]
            readpath_2 = all_paths[counter+8]
        image = cv2.imread(readpath)
        image_2 = cv2.imread(readpath_2)
        image = cv2.resize(image, (800,800))
        image_2 = cv2.resize(image_2, (800,800))

        def blur_and_threshold(gray):
            gray = cv2.GaussianBlur(gray,(3,3),2)#
            threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            threshold = cv2.fastNlMeansDenoising(threshold, 11, 31, 9)
            return threshold

        def biggest_contour(contours,min_area):
            biggest = None
            max_area = 0
            biggest_n=0
            approx_contour=None
            for n,i in enumerate(contours):
                    area = cv2.contourArea(i)         
            
                    if area > min_area/5:
                            peri = cv2.arcLength(i,True)
                            approx = cv2.approxPolyDP(i,0.02*peri,True)
                            if area > max_area and len(approx)==4:
                                    biggest = approx
                                    max_area = area
                                    biggest_n=n
                                    approx_contour=approx                            
                                                   
            return biggest_n,approx_contour

        def order_points(pts):
            pts=pts.reshape(4,2)
            rect = np.zeros((4, 2), dtype = "float32")
            s = pts.sum(axis = 1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis = 1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            return rect

        def four_point_transform(image, pts):
            rect = order_points(pts)
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            maxWidth = max(int(widthA), int(widthB))
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            maxHeight = max(int(heightA), int(heightB))
            dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
            return warped


        def transformation(image,image_2):
            image=image.copy()  
            image_2=image_2.copy()  
            height, width, channels = image.shape
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            image_size=gray.size    
            threshold=blur_and_threshold(gray)
            edges = cv2.Canny(threshold,150,150,apertureSize = 7)
            if counter < 4:
                cv2.imwrite(path + "\Canny_Image_" + str(counter+1) + "b.jpg", edges)
            elif (counter >= 4) and (counter < 8):
                cv2.imwrite(path + "\Canny_Image_" + str(counter-3) + "a.jpg", edges)
            elif (counter >= 8) and (counter < 12):
                cv2.imwrite(path + "\Canny_Image_" + str(counter-3) + "b.jpg", edges)
            else:
                cv2.imwrite(path + "\Canny_Image_" + str(counter-7) + "a.jpg", edges)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            simplified_contours = []


            for cnt in contours:
                hull = cv2.convexHull(cnt)
                simplified_contours.append(cv2.approxPolyDP(hull,0.001*cv2.arcLength(hull,True),True))
            simplified_contours = np.array(simplified_contours,dtype=object)
            biggest_n,approx_contour = biggest_contour(simplified_contours,image_size)

            threshold = cv2.drawContours(image, simplified_contours ,biggest_n, (0,255,0), 1)
            threshold_2 = cv2.drawContours(image_2, simplified_contours ,biggest_n, (0,255,0), 1)

            dst = 0
            if approx_contour is not None and len(approx_contour)==4:
                approx_contour=np.float32(approx_contour)
                dst=four_point_transform(threshold,approx_contour)
            dst1 = 0
            if approx_contour is not None and len(approx_contour)==4:
                approx_contour=np.float32(approx_contour)
                dst1=four_point_transform(threshold_2,approx_contour)
            croppedImage = dst
            croppedImage1 = dst1
            return croppedImage,croppedImage1

        def increase_brightness(img, value=30):
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
            final_hsv = cv2.merge((h, s, v))
            img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            return img  

        def final_image(rotated):
          kernel_sharpening = np.array([[0,-1,0], 
                                [-1, 5,-1],
                                [0,-1,0]])
          sharpened = cv2.filter2D(rotated, -1, kernel_sharpening)
          sharpened=increase_brightness(sharpened,30)  
          return sharpened

        blurred_threshold, blurred_threshold_2 = transformation(image,image_2)
        cleaned_image_before.append(final_image(blurred_threshold))
        cleaned_image_after.append(final_image(blurred_threshold_2))

    for cnt in range(0,int(len(all_paths)/2)):
        scan_and_crop(cnt)

    return cleaned_image_before, cleaned_image_after