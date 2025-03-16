import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from faker import Faker
import os

# Initialize Faker for random number plate text
fake = Faker()

# Function to add maximum fog to an image
def add_max_fog(image):
    # Create a white layer with the same size as the image
    fog_layer = np.ones_like(image) * 255  # White layer (maximum fog)
    
    # Blend the image with the fog layer (70% opacity for maximum fog)
    foggy_image = cv2.addWeighted(image, 0.3, fog_layer, 0.7, 0)
    
    return foggy_image

# Function to generate random number plate text
def generate_number_plate():
    return fake.license_plate()

# Function to overlay number plate on an image and make it blurry
def add_number_plate(image, text, position=(220, 420), font_size=40):
    image_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(image_pil)
    
    # Load a larger font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Use a system font like Arial
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font
    
    # Calculate text bounding box
    text_bbox = draw.textbbox(position, text, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # Calculate text width
    text_height = text_bbox[3] - text_bbox[1]  # Calculate text height
    
    # Draw a background rectangle for the number plate
    background_position = (
        position[0] - 10,  # Add padding
        position[1] - 10,  # Add padding
        position[0] + text_width + 10,  # Add padding
        position[1] + text_height + 10  # Add padding
    )
    draw.rectangle(background_position, fill=(0, 0, 0))  # Black background
    
    # Draw the number plate text
    draw.text(position, text, font=font, fill=(255, 255, 255))  # White text
    
    # Convert the image back to a NumPy array
    image_with_plate = np.array(image_pil)
    
    # Apply Gaussian blur to the number plate region to make it blurry and hazy
    blur_kernel_size = (25, 25)  # Increased kernel size for more blur
    blurred_plate = cv2.GaussianBlur(image_with_plate, blur_kernel_size, 0)
    
    # Blend the blurred number plate region back into the original image
    x1, y1, x2, y2 = background_position
    image_with_plate[y1:y2, x1:x2] = blurred_plate[y1:y2, x1:x2]
    
    return image_with_plate

# Function to process a dataset of images
def process_dataset(dataset_path, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop through all images in the dataset
    for filename in os.listdir(dataset_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Add other formats if needed
            # Load the image
            image_path = os.path.join(dataset_path, filename)
            image = cv2.imread(image_path)
            
            if image is not None:
                # Add a random number plate
                number_plate_text = generate_number_plate()
                image_with_plate = add_number_plate(image, number_plate_text)
                
                # Add maximum fog after adding the number plate
                foggy_image = add_max_fog(image_with_plate)
                
                # Save the processed image
                output_path = os.path.join(output_dir, f"processed_{filename}")
                cv2.imwrite(output_path, foggy_image)
                print(f"Saved: {output_path}")
            else:
                print(f"Failed to load image: {image_path}")

# Main function to process the dataset
def main():
    # Path to your dataset
    dataset_path = "generated_images"  # Replace with the path to your dataset folder
    
    # Path to save processed images
    output_dir = "synthetic_images3"
    
    # Process the dataset
    process_dataset(dataset_path, output_dir)

if __name__ == "__main__":
    main()