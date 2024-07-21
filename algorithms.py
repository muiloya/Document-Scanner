import cv2
import numpy as np
import matplotlib.pyplot as plt

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

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

    # Unsharp Masking
    img_smooth = unsharp_mask(image_gray_scale)
    results.append(img_smooth)
    titles.append("Unsharp Masked")

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

    #Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    equalized_img = clahe.apply(corrected_image)
    results.append(equalized_img)
    titles.append("Histogram Equalization")

    # Binarization
    _, thresh_img = cv2.threshold(equalized_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    results.append(thresh_img)
    titles.append("Binarization")

    # Morphological Operations
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    opened_image = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel)
    results.append(opened_image)
    titles.append("Morphological Operations")

    # Returning all processed images
    return results , titles

def display_images(images, titles):
    n = len(images)
    plt.figure(figsize=(30, 10))

    for i in range(n):
        plt.subplot(2, (n + 1) // 2, i + 1)
        if len(images[i].shape) == 2:  # Grayscale image
            plt.imshow(images[i], cmap='gray')
        else:  # Color image
            plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
        plt.title(titles[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()
