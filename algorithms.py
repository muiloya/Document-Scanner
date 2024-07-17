import cv2

def process_pipeline(img):
    image_gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## could be any smoothing filter
    img_smooth = cv2.GaussianBlur(img, (5, 5), 0)

    ## will need to experiment with different kernels
    sharpened_image = cv2.filter2D(image, -1, kernel)

    ## edge detection
    sobel_image = cv2.Sobel(img, cv2.CV_64F, 1, 1, 5)

    ##Hough Transform

    ## histogram
    equalized_img = cv2.equalizeHist(img)

    ## binarizing
    ret, thresh_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    ## morphological operations
    dilated_image = cv2.dilate(binary_image, kernel, iterations=1)

    return processed_img