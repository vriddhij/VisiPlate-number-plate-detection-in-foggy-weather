import cv2
import torch
import numpy as np
import torchvision.transforms as transforms
from dehazenet import DehazeNet

# Enhance contrast & suppress shadows
def enhance_image(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return enhanced

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DehazeNet().to(device)
model.eval()

# Transform input frame
transform = transforms.Compose([
    transforms.ToTensor()
])

# Start webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow("Original vs Dehazed", cv2.WINDOW_NORMAL)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        input_img = cv2.resize(frame, (224, 224))
        input_tensor = transform(input_img).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(input_tensor)

        # Convert model output to image
        output_img = output.squeeze().permute(1, 2, 0).cpu().numpy()
        output_img = (output_img * 255).astype('uint8')
        output_resized = cv2.resize(output_img, (frame.shape[1], frame.shape[0]))

        # Apply contrast enhancement
        enhanced = enhance_image(output_resized)

        # Combine original and dehazed
        combined = cv2.hconcat([frame, enhanced])
        cv2.imshow('Original vs Dehazed', combined)

        # Exit if 'q' is pressed or window closed
        key = cv2.waitKey(1)
        if key == ord('q') or cv2.getWindowProperty('Original vs Dehazed', cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
