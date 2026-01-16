```
Aim : 
Use CV techniques to detect an object in motion in a video

Process:
• Read the frame
• Preprocess with gaussian blur
• Seperate moving region from static background and make a mask using bgSub
• Stabilize the mask using closing and opening
• Then apply canny to get all the edges of the moving part
• Obtain contours of the outermost edges
• Finding the contour with the most motion - 
    Calculate centroid of each contour in the moving region and compare centroids of the contour in two consecutive frames
    Whichever contour has the maximum motion is the detected contour
• Draw bounding box,convex hull, outline and trajectory for the detected contour. 
```
