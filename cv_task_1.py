import cv2
import numpy as np
thickness=3
max_points=5
valid_contour_area=500
# capture=cv2.VideoCapture(0)
capture=cv2.VideoCapture('vid1.mp4')
bgSub=cv2.createBackgroundSubtractorMOG2(
    history=500, 
    varThreshold=200, 
    detectShadows=False
)

trajectory=[]
prev_centroids=(0, 0)

while True:
    _, frame=capture.read() #frame acquisition
    preprocess = cv2.GaussianBlur(frame, (5, 5), 0)
    fgMask=bgSub.apply(preprocess, learningRate=1e-3) #seperating static and moving regions (I'm aware that the pipeline asks to do canny first, refer the readme for the reason i did this)
    kernel=np.ones((5, 5), np.uint8)
    stable=cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel) #stabilize and clean the obtained mask
    stable=cv2.morphologyEx(stable, cv2.MORPH_OPEN, kernel)
    edges=cv2.Canny(stable, 60, 180) #obtain edges
    contours, _=cv2.findContours(edges, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE) #obtain contours
    if len(contours)>0:
        valid_contours=[contour for contour in contours if cv2.contourArea(contour)>valid_contour_area] #avoid noise and only consider real contours
        current_centroids=[]
        if valid_contours: #centroid calculation - refer readme
            for contour in valid_contours:
                M=cv2.moments(contour)
                curr_centroid=(int(M['m10']/M['m00']), int(M['m01']/M['m00'])) #calculating all the contour centroids
                current_centroids.append((curr_centroid, contour))
        min_distance=float('inf')
        detected_contour=None
        detected_centroid=None
        if prev_centroids and current_centroids:
            for point, contour in current_centroids:
                distance=np.sqrt((point[0]-prev_centroids[0])**2 + (point[1]-prev_centroids[1])**2) #finding centroid shift for the same contour in two consecutive frames
                if min_distance>distance:
                    min_distance=distance
                    detected_contour=contour
                    detected_centroid=point
        elif valid_contours:
            detected_contour=max(valid_contours, key=cv2.contourArea) #for the first frame alone, just taking detected biggest contour, because there's no previous contour 
            M=cv2.moments(detected_contour)
            detected_centroid=(int(M['m10']/M['m00']), int(M['m01']/M['m00']))
            
        if detected_contour is not None: ##visualization
            x, y, w, h = cv2.boundingRect(detected_contour) 
            cv2.rectangle(frame, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=thickness) #bounding box
            cv2.drawContours(frame, [detected_contour],-1, color=(0, 255, 0), thickness=thickness) #contour outline
            hull=cv2.convexHull(detected_contour)
            cv2.drawContours(frame, [hull], -1, (255, 0, 0), thickness=thickness) #convex hull
            M=cv2.moments(detected_contour)
            if M["m00"] !=0:
                cx=int(M["m10"]/M["m00"])
                cy=int(M["m01"]/M["m00"])
                trajectory.append((cx, cy))
            if len(trajectory)>max_points:trajectory.pop(0)
            for i in range(1, len(trajectory)):
                cv2.line(frame, trajectory[i-1], trajectory[i], color=(255, 255, 255), thickness=thickness) #centroid trajectory
        if current_centroids:
            prev_centroids=detected_centroid
    cv2.imshow("final", frame)
    cv2.imshow("mask", stable)
    key=cv2.waitKey(30)
    if key == ord('x'): exit()

