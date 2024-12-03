import os
import cv2
import numpy as np
import pytesseract


def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Preprocess the image
    preprocessed_image = preprocess_image(image)
    
    # Detect the orientation
    rotation_angle = detect_orientation(preprocessed_image)
    
    # Rotate the image
    rotated_image = rotate_image(image, rotation_angle)
    
    return rotated_image

def rotate_image(image, angle):
    # Get the image dimensions
    height, width = image.shape[:2]
    
    # Calculate the center of the image
    center = (width // 2, height // 2)
    
    # Create the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Perform the rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated_image

   
def detect_orientation(image):
    # Set the Tesseract OCR configuration to detect the orientation
    config = "--psm 0"
    
    # Run Tesseract OCR to detect the orientation
    orientation_data = pytesseract.image_to_osd(image, config=config)
    
    # Extract the rotation angle from the orientation data
    rotation_angle = int(orientation_data.split("\n")[2].split(":")[1].strip())
    
    return rotation_angle

def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to create a binary image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Apply morphological operations to remove noise
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return binary

def process_identity_documents(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            rotated_image = process_image(image_path)
            
            # Convert the image to RGB mode before saving
            rgb_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
            cv2.imwrite(image_path, cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))
            
            print(f"Processed: {filename}")

# Directory containing the identity documents
identity_documents_dir = "identity_documents"

# Process all the photos in the directory
process_identity_documents(identity_documents_dir)