# msbdn2.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

def defog_image(img):
    # Simple placeholder: increase contrast (you can replace this with your model)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0)
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    final = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    return final

def upload_and_defog():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if not file_path:
        return

    img = cv2.imread(file_path)
    defogged = defog_image(img)

    # Convert to PIL Image and show
    defogged_rgb = cv2.cvtColor(defogged, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(defogged_rgb)
    pil_img.show()

# GUI
root = tk.Tk()
root.title("Defog Image")
root.geometry("400x200")

label = tk.Label(root, text="Upload an image to defog it", font=("Helvetica", 14))
label.pack(pady=20)

btn = tk.Button(root, text="Upload Image", command=upload_and_defog, font=("Helvetica", 12), bg="black", fg="white")
btn.pack(pady=20)

root.mainloop()
