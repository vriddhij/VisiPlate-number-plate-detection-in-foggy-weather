import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from faker import Faker
import os

# Initialize Faker for random number plate text
fake = Faker()

# Function to create a synthetic vehicle-like image
def create_synthetic_vehicle(width=640, height=480):
    # Create a blank image
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw a rectangle (representing the vehicle body)
    cv2.rectangle(image, (100, 200), (540, 400), (0, 0, 255), -1)  # Red rectangle
    
    # Draw circles (representing wheels)
    cv2.circle(image, (150, 400), 30, (0, 0, 0), -1)  # Black wheel
    cv2.circle(image, (490, 400), 30, (0, 0, 0), -1)  # Black wheel
    
    return image

# Function to add maximum fog to an image
def add_max_fog(image):
    # Create a white layer with the same size as the image
    fog_layer = np.ones_like(image) * 255  # White layer (maximum fog)
    
    # Blend the image with the fog layer (50% opacity for maximum fog)
    foggy_image = cv2.addWeighted(image, 0.5, fog_layer, 0.5, 0)
    
    return foggy_image

# Function to generate random number plate text
def generate_number_plate():
    return fake.license_plate()

# Function to overlay number plate on an image
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
    
    return np.array(image_pil)

# Generate synthetic foggy images with number plates
def generate_synthetic_data(num_samples=1000):
    synthetic_data = []
    for _ in range(num_samples):
        # Create a synthetic vehicle image
        vehicle_image = create_synthetic_vehicle()
        
        # Add maximum fog
        foggy_image = add_max_fog(vehicle_image)
        
        # Add a random number plate
        number_plate_text = generate_number_plate()
        synthetic_image = add_number_plate(foggy_image, number_plate_text)
        
        synthetic_data.append(synthetic_image)
    
    return synthetic_data

# Main function to generate and save synthetic data
def main():
    # Generate synthetic data
    synthetic_data = generate_synthetic_data(num_samples=1000)

    # Save synthetic images
    output_dir = "generated_images"
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

    for idx, image in enumerate(synthetic_data):
        output_path = os.path.join(output_dir, f"synthetic_{idx}.jpg")
        cv2.imwrite(output_path, image)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()