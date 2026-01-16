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

Reason to deviate from the given pipeline:
    Im aware that the given pipeline is 
        frame acquisition -> canny edge detection -> stabilization -> object isolation -> contour detection
    what i did is 
        frame acquisition -> object isolation -> stabilization -> canny edge detection -> contour detection

    when i apply canny on the raw frame, it gives a binary of every minimal edge on the frame which contains a lot of noise, and bg mask expects an rgb frame because it basically learns from the pixel values if something is foreground or background right and all of this is resulting in a less accurate output. So i thought as canny detects edges according to the sudden increase in pixel values, it could take the stabilized mask and detect edges of the moving part.
    Also applying canny on raw frame is a bit of too much computation and was making the output a bit choppy. 

```
