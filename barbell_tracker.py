import cv2
import numpy as np

# For OpenCV2 image display
WINDOW_NAME = 'BarbellTracker' 

def track(image):

    '''Accepts RGB image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert RGB to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    lower_green = np.array([40,70,70])
    upper_green = np.array([80,200,200])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)

        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 5, (0,0,0))


    # Display full-color image
    cv2.imshow(WINDOW_NAME, image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None

    # Return coordinates of centroid
    return centroid_x

# Test with input from camera
if __name__ == '__main__':

    capture = cv2.VideoCapture(0)

    while True:

        okay, image = capture.read()

        if okay:

            c_x = track(image)
            
            if track(image) != c_x:
                print "\a"
                  
            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:

           print('Capture failed')
           break
