import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

image_path = None
original_image = None
img = None
ax = None
canvas = None
threshold_applied = False
processed_image = None

def apply_threshold():
    global threshold_applied, processed_image
    try:
        if img is not None:
            threshold = threshold_slider.get()
            processed_image = process_image(threshold)
            update_display(processed_image)
            threshold_applied = True
    except Exception as e:
        print(e)

def remove_threshold():
    global threshold_applied
    try:
        if img is not None and threshold_applied:
            update_display(original_image)
            threshold_applied = False
    except Exception as e:
        print(e)

def remove_changes():
    global original_image
    if original_image is not None:
        update_display(original_image)

def blur_image():
    global img, original_image
    if img is not None:
        original_image = img.copy()
        img_blurred = img.filter(ImageFilter.GaussianBlur(radius=8))
        update_display(img_blurred)

def sharp_image():
    global img, original_image
    if img is not None:
        original_image = img.copy()
        img_sharpened = img.filter(ImageFilter.SHARPEN)
        update_display(img_sharpened)

def process_image(threshold):
    global img
    img_gray = img.convert("L")
    img_thresholded = img_gray.point(lambda p: p > threshold and 255)
    return img_thresholded

def convert_to_grayscale():
    global img, original_image
    if img is not None:
        original_image = img.copy()
        img_gray = img.convert("L")
        update_display(img_gray)

def update_display(image):
    ax.imshow(image, cmap='gray')
    canvas.draw()

def open_file():
    global image_path, img, original_image
    image_path = filedialog.askopenfilename()
    img = Image.open(image_path)
    original_image = img.copy()
    update_display(img)

root = tk.Tk()
root.title("PythonShop")

frame = tk.Frame(root)
frame.pack()

button_frame = tk.Frame(frame)
button_frame.pack()

threshold_label = tk.Label(button_frame, text="Threshold:")
threshold_label.pack(side=tk.LEFT)

threshold_slider = tk.Scale(button_frame, from_=0, to=255, orient=tk.HORIZONTAL)
threshold_slider.set(127)

threshold_slider.pack(side=tk.LEFT)

apply_button = tk.Button(button_frame, text="Apply Threshold", command=apply_threshold, fg="blue")
apply_button.pack(side=tk.LEFT)

grayscale_button = tk.Button(button_frame, text="Convert to Grayscale", command=convert_to_grayscale, fg="blue")
grayscale_button.pack(side=tk.LEFT)

blur_button = tk.Button(button_frame, text="Blur Image", command=blur_image, fg="blue")
blur_button.pack(side=tk.LEFT)

sharp_button = tk.Button(button_frame, text="Sharp Image", command=sharp_image, fg="blue")
sharp_button.pack(side=tk.LEFT)

open_button = tk.Button(frame, text="Open Image", command=open_file, fg="green")
open_button.pack(side=tk.LEFT)

remove_button = tk.Button(frame, text="Remove", command=remove_changes, fg="red")
remove_button.pack(side=tk.LEFT)



fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
