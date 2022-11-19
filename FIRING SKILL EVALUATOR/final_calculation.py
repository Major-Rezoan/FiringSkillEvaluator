import cv2
import os
import numpy as np
from shooting_errors_Ellipse import directional_error
from corrections import put_corrections

def calc_result(ssi_images, ssi_processed_masks):

    indl_groups = []
    indl_errors = []

    def calculate_Result(imgNo):
        mask_image = ssi_processed_masks[imgNo]
        shortest_distance=[]

        def load_and_preprocess(inp_image=None, width=400, height=400, threshold=128):
            img = inp_image
            img = cv2.resize(img, (width, height))
            img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]
            return img


        def smoothing_bulletmark(img, kernel_size):
            kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
            img = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)
            return img


        def disp_line_point(center=None, points=None, input_image=None, window_name="Image Display"):
            img = input_image
            img = cv2.resize(img, (400, 400))
            cv2.line(img, points[0], points[1], (255, 0, 0), 2)
            cv2.circle(img, center=center, radius=3, color=(0, 0, 255), thickness=1)
        def disp_impact_points(center, window_name):
            img = np.ones([400,400,3], dtype='uint8')
            img[:,:,0] = np.ones([400,400])*125
            img[:,:,1] = np.ones([400,400])*255
            img[:,:,2] = np.ones([400,400])*210
            impact_img = img
            for i in range(0, 5):
                    impact_img=cv2.circle(impact_img, center=center[i], radius=2, color=(i*30,i*20,255), thickness=2)
            return impact_img


        def find_coordinates(img_thresh, connectivity=4):
            img_neg = abs(img_thresh[:,:,0] - 255)
            numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_neg, connectivity, cv2.CV_32S)
            points = []
            for centroid, stat in zip(centroids, stats):
                if stat[3] < 50:
                    points.append((int(centroid[0]), int(centroid[1])))
            return points

        def calc_diameter(points, display=True):
            diameter = -1
            gp_center = None
            for point1 in points:
                for point2 in points:
                    if point1 != point2:
                        dist = int(np.linalg.norm(np.array(point1) - np.array(point2)))
                        center = (np.array(point1) + np.array(point2)) // 2
                        if dist > diameter:
                            diameter = dist
                            max_points = [point1, point2]
                            gp_center = center
                        if display:
                            disp_line_point(center=center, points=[point1, point2], image=mask_image,
                                    window_name="GP Calculation")
            return diameter, max_points, gp_center

        def find_closest_pair(points, center=None):
            img = mask_image
            img = cv2.resize(img, (400, 400))

            min_dist = 1500
            mpi = None
            if center is None:
                for point1 in points:
                    for point2 in points:
                        if point1 != point2:
                            dist = int(np.linalg.norm(np.array(point1) - np.array(point2)))
                            center = (np.array(point1) + np.array(point2)) // 2
                            if dist < min_dist:
                                min_dist = dist
                                min_points = [point1, point2]
                                mpi = center
                points.remove(min_points[0])
                points.remove(min_points[1])
            else:
                for point in points:
                    dist = int(np.linalg.norm(np.array(center) - np.array(point)))
                    center_new = (np.array(center) + np.array(point)) // 2
                    if dist < min_dist:
                        min_dist = dist
                        min_points = [center, point]
                        mpi = center_new
                points.remove(min_points[1])

            shortest_distance.append(min_dist)
            return min_dist, min_points, mpi, points


        def calc_MPI(points, display=True):
            min_dist, min_points, center, rem_points = find_closest_pair(points)
            while len(rem_points):
                min_dist, min_points, center, rem_points = find_closest_pair(points, center=center)
            return center


        def display_result(input_image, points, gp_center, mpi_center, group, distbull,  horidist, vertdist, error_name, display=False):
            gpimg = input_image
            gpimg = cv2.resize(gpimg, (400, 400))
            for i in range(0, 5):
                gpimg=cv2.circle(gpimg, center=points[i], radius=2, color=(10+(i*5), i*10, 255), thickness=2)
            gpimg = cv2.resize(gpimg, (800, 800))
            blank = np.ones(gpimg.shape, dtype='uint8')
            img = np.concatenate((gpimg, blank), axis=1)

            color = (5, 220, 215)
            thickness = 3
            img = cv2.circle(img, gp_center*2, int(group * 400 / 48) + 4, color, thickness)

            woresult = ''
            if group > 10.5:
                woresult = ' (Washed Out)'
                class_name = 'Washed Out'
            elif group <= 10.5 and group > 7.5:
                class_name = 'Standard Shot'
            elif group <= 7.5 and group > 4.5:
                class_name = '1st Class Shot'
            else:
                class_name = 'Marksman Shot'

            st_group = str(group)
            text = "Grouping: " + st_group + " inches" + woresult
            radius = 5
            thickness = 4
            gp_color = (5, 220, 215)
            gp_color_b = (5, 95, 230)
            mpi_color = (230, 195, 5)
            mpi_color_b = (215, 45, 150)
            img = cv2.circle(img, gp_center*2, radius+4, gp_color_b, thickness+2)
            img = cv2.circle(img, gp_center*2, radius, gp_color, thickness)
            img = cv2.circle(img, mpi_center*2, radius+4, mpi_color_b, thickness+2)
            img = cv2.circle(img, mpi_center*2, radius, mpi_color, thickness)
            font = cv2.FONT_HERSHEY_SIMPLEX
            gp_font = cv2.FONT_HERSHEY_COMPLEX
            org = (820, 50)
            fontScale = 1.2
            if group > 11:
                gp_text_color = (10, 10, 250)
            else:
                gp_text_color = (10, 250, 10)
            thickness = 2
            img = cv2.putText(img, text, org, gp_font, fontScale, gp_text_color, thickness, cv2.LINE_AA)
            org = (820, 100)
            img = cv2.circle(img, (830, 92), radius+4, gp_color_b, thickness+2)
            img = cv2.circle(img, (830, 92), radius, gp_color, thickness)
            fontScale = 0.8
            thickness = 2
            img = cv2.putText(img, '  --> Center of the Group', org, font, fontScale, gp_color, thickness, cv2.LINE_AA)
            org = (820, 130)
            img = cv2.circle(img, (830, 123), radius+4, mpi_color_b, thickness+2)
            img = cv2.circle(img, (830, 123), radius, mpi_color, thickness)
            fontScale = 0.8
            thickness = 2
            img = cv2.putText(img, '  --> Mean Point of Impact', org, font, fontScale, mpi_color, thickness, cv2.LINE_AA)
            org = (820, 160)
            fontScale = 0.8
            color = (255, 255, 0)
            thickness = 2
            distbull = distbull * 48 / 400
            img = cv2.putText(img, 'Distance from center: ' + str(distbull) + ' inches', org, font, fontScale, color, thickness, cv2.LINE_AA)
            horidist = horidist / 8.2
            vertdist = vertdist / 6.2

            corr_vert = "upwards"
            if(vertdist + vertdist < 0):
                vertdist = vertdist * -1
                corr_vert = "downwards"

            corr_hori = "right"
            if(horidist + horidist < 0):
                horidist = horidist * -1
                corr_hori = "left"

            horidist = "{:.2f}".format(horidist)
            vertdist = "{:.2f}".format(vertdist)

            org = (820, 190)
            fontScale = 0.8
            color = (255, 200, 100)
            thickness = 2
            img = cv2.putText(img, 'Vertical correction: ' + str(vertdist) + ' rotation ' + corr_vert, org, font, fontScale, color, thickness, cv2.LINE_AA)
    
            org = (820, 220)
            fontScale = 0.8
            color = (255, 100, 200)
            thickness = 2
            img = cv2.putText(img, 'Horizontal correction: ' + str(horidist) + ' mm towards ' + corr_hori, org, font, fontScale, color, thickness, cv2.LINE_AA)

            org = (820, 250)
            fontScale = 0.8
            color = (75, 200, 200)
            thickness = 2
            img = cv2.putText(img, 'Classification: ' + str(class_name), org, font, fontScale, color, thickness, cv2.LINE_AA)

            org = (820, 280)
            fontScale = 0.8
            color = (150, 150, 200)
            thickness = 2
            img = cv2.putText(img, 'Error Name: ' + str(error_name), org, font, fontScale, color, thickness, cv2.LINE_AA)

            if error_name != 'No Listed Error':
                error_name = error_name.split("/")
                if (len(error_name) <= 1):
                    put_corrections(img, error_name[0], 310)
                else:
                    put_corrections(img, error_name[0], 310)
                    put_corrections(img, error_name[1], 500)

            directory = "data_final/"
            filename = directory + 'FiringResult' + str(imgNo+1) + '.jpg'
            cv2.imwrite(filename, img)

            if display:
                cv2.imshow("Result Visualization", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


        input_mask_image = mask_image
        img = load_and_preprocess(input_mask_image)
        proc_img = smoothing_bulletmark(img, kernel_size=3)
        points = find_coordinates(proc_img)
        if len(points) < 5:
            i=2
            while len(points) != 5:
                proc_img = smoothing_bulletmark(img, kernel_size=i)
                points = find_coordinates(proc_img) 
                i+=1
        else:
            i=10
            while len(points) != 5:
                proc_img = smoothing_bulletmark(img, kernel_size=i)
                points = find_coordinates(proc_img) 
                i-=1
            
        img_for_error = disp_impact_points(points, window_name='Impact Points')

        diameter, max_points, gp_center = calc_diameter(points.copy(), display=False)
        mpi_center = calc_MPI(points.copy())
        dist = int(np.linalg.norm(np.array(gp_center) - np.array(mpi_center)))
        group = diameter * 48 / 400
        indl_groups.append(group)
        distbull = int(np.linalg.norm(np.array(mpi_center) - np.array(200)))
        horidist = (mpi_center[0] - 200) * 48 / 400
        vertdist = (200 - mpi_center[1]) * 48 / 400

        max_distance = max(shortest_distance)
        last_distance = shortest_distance[3]
        distances = shortest_distance
        distances.remove(max_distance)

        error_name, error_img = directional_error(img_for_error, points, distances, max_distance, last_distance, group)
        indl_errors.append(error_name)

        disp_image = ssi_images[imgNo]
        display_result(disp_image, points, gp_center, mpi_center, group, distbull, horidist, vertdist, error_name, False)

        directory = "data_final/"
        filename = directory + 'Error' + str(imgNo+1) + '.jpg'
        cv2.imwrite(filename, error_img)

    for i in range(0,len(ssi_images)):
        calculate_Result(i)
    return indl_groups, indl_errors



