import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import albumentations as A
from faker import Faker
import os

# Initialize Faker for random number plate text
fake = Faker()

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
def add_number_plate(image, text, position=(50, 50), font_size=40):
    image_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(image_pil)
    font = ImageFont.load_default()  # You can use a custom font here
    draw.text(position, text, font=font, fill=(255, 255, 255))
    return np.array(image_pil)

# Generate synthetic foggy images with number plates
def generate_synthetic_data(real_images, num_samples=20):
    synthetic_data = []
    for image in real_images:
        # Add maximum fog
        foggy_image = add_max_fog(image)
        
        # Add a random number plate
        number_plate_text = generate_number_plate()
        synthetic_image = add_number_plate(foggy_image, number_plate_text)
        
        synthetic_data.append(synthetic_image)
    
    return synthetic_data

# Load your dataset
def load_dataset(dataset_path):
    real_images = []
    for filename in os.listdir(dataset_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Add other formats if needed
            image_path = os.path.join(dataset_path, filename)
            image = cv2.imread(image_path)
            if image is not None:
                # Resize images to a smaller resolution to save memory
                image = cv2.resize(image, (640, 480))  # Resize to 640x480 (adjust as needed)
                real_images.append(image)
            else:
                print(f"Failed to load image: {image_path}")
    print(f"Loaded {len(real_images)} images from the dataset.")
    return real_images

# Main function to generate and save synthetic data
def main():
    # Path to your dataset
    dataset_path = "synthetic_images2" # Replace with the path to your dataset folder

    # Check if the dataset path exists
    if not os.path.exists(dataset_path):
        print(f"Dataset path does not exist: {dataset_path}")
        return

    # Load your dataset
    real_images = load_dataset(dataset_path)

    # Check if any images were loaded
    if len(real_images) == 0:
        print("No images were loaded. Check the dataset path and image formats.")
        return

    # Generate synthetic data
    synthetic_data = generate_synthetic_data(real_images, num_samples=20)

    # Save synthetic images
    output_dir = "synthetic_images3"
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

    for idx, image in enumerate(synthetic_data):
        output_path = os.path.join(output_dir, f"synthetic_{idx}.jpg")
        cv2.imwrite(output_path, image)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()