import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_pipeline(image_path):
    results=[]
    titles=[]

    #Original
    img = cv2.imread(image_path)
    results.append(img)
    titles.append("Original")

    # Grayscale
    image_gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results.append(image_gray_scale)
    titles.append("Grayscale")

    # Smoothing
    img_smooth = cv2.GaussianBlur(image_gray_scale, (3, 3), 0)
    results.append(img_smooth)
    titles.append("Smoothed")

    # Edge Detection
    edges = cv2.Canny(img_smooth, 50, 150, apertureSize=3)
    results.append(edges)
    titles.append("Edges")

    # Hough Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    angles = [np.degrees(line[0][1]) - 90 for line in lines]
    mode_angle = np.median(angles)
    skew_angle = mode_angle - 90 if mode_angle > 45 else (mode_angle + 90 if mode_angle < -45 else mode_angle)
    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), skew_angle, 1.0)
    corrected_image = cv2.warpAffine(img_smooth, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    results.append(corrected_image)
    titles.append("Skew Correction")

    # Sharpening
    sharpening_kernel = np.array([[0, 1, 0],
                                  [1, -4, 1],
                                  [0, 1, 0]])
    sharpened_image = cv2.filter2D(corrected_image, -1, sharpening_kernel)
    sharpened_image=cv2.addWeighted(corrected_image, 1.0, sharpened_image, 1.0, 0)
    results.append(sharpened_image)
    titles.append("Sharpened")

    # Histogram Equalization
    #equalized_img = cv2.equalizeHist(corrected_image)

    # Binarization
    _, thresh_img = cv2.threshold(sharpened_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(thresh_img)
    titles.append("Binarization")

    # Morphological Operations
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(thresh_img, kernel, iterations=1)
    results.append(dilated_image)
    titles.append("Morphological Operations")

    # Returning all processed images
    return results , titles

def display_images(images, titles):
    n = len(images)
    plt.figure(figsize=(20, 10))

    for i in range(n):
        plt.subplot(2, (n + 1) // 2, i + 1)
        plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()
