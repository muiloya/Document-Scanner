import cv2
import numpy as np

def process_pipeline(image_path):
    
    img = cv2.imread(image_path)

    image_gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## could be any smoothing filter
    img_smooth = cv2.GaussianBlur(image_gray_scale, (5, 5), 0)

    sharpening_kernel = np.array([[0, -1, 0],
                    [-1, 4, -1],
                    [0, -1, 0]])

    # Apply the sharpening filter
    sharpened_image = cv2.filter2D(img_smooth, -1, sharpening_kernel)

    ## edge detection
    edges = cv2.Canny(sharpened_image, 50, 150, apertureSize=3) 

    ##Hough Transform
    lines = cv2.HoughLines (edges, 1, np.pi / 180, 200)
    
    # Calculate angles of the lines
    angles = []
    for line in lines:
        rho, theta = line[0]
        angle = np.degrees (theta) - 90
        angles.append(angle)
    # Find the most common angle (mode) and adjust to the closest 90 degree angle
    mode_angle = np.median (angles)
    if mode_angle > 45:
        skew_angle = mode_angle - 90
    elif mode_angle < -45:
        skew_angle = mode_angle + 90
    else:
        skew_angle = mode_angle
    # Rotate the image to correct the skew
    (h, w) = img.shape[:2]
    center= (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, skew_angle, 1.0)
    corrected_image = cv2.warpAffine(image_gray_scale, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    ## histogram
    equalized_img = cv2.equalizeHist(img)

    ## binarizing
    ret, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    ## morphological operations

    dilated_image = cv2.dilate(thresh_img, kernel, iterations=1)

    return processed_img