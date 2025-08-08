import os
import random
import matplotlib.pyplot as plt
import cv2
from ultralytics import YOLO
from PIL import Image

# Disable warnings in the notebook to maintain clean output cells
import warnings
warnings.filterwarnings('ignore')
from IPython import display
display.clear_output()
train_images = "C:\\Users\\Administrator\\PyCharmMiscProject\\j\\train\\images"
train_labels = "C:\\Users\\Administrator\\PyCharmMiscProject\\j\\train\\labels"

# Get a list of all the image files in the training images directory
image_files = os.listdir(train_images)

# Choose 6 random image files from the list
random_images = random.sample(image_files, 6)

# Set up the plot
fig, axs = plt.subplots(2, 3, figsize=(12, 8))

# Load class names
class_names = {
    0: 'Green Light',
    1: 'Red Light',
    2: 'Speed Limit 10',
    3: 'Speed Limit 100',
    4: 'Speed Limit 110',
    5: 'Speed Limit 120',
    6: 'Speed Limit 20',
    7: 'Speed Limit 30',
    8: 'Speed Limit 40',
    9: 'Speed Limit 50',
    10:'Speed Limit 60',
    11:'Speed Limit 70',
    12:'Speed Limit 80',
    13:'Speed Limit 90',
    14:'Stop'
}

for i, image_file in enumerate(random_images):
    row = i // 3
    col = i % 3

    # Load the image
    image_path = os.path.join(train_images, image_file)
    image = cv2.imread(image_path)

    # Load the labels for this image
    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join(train_labels, label_file)
    with open(label_path, "r") as f:
        labels = f.read().strip().split("\n")

    # Loop over the labels and plot the object detections
    for label in labels:
        if len(label.split()) != 5:
            continue
        class_id, x_center, y_center, width, height = map(float, label.split())
        x_min = int((x_center - width/2) * image.shape[1])
        y_min = int((y_center - height/2) * image.shape[0])
        x_max = int((x_center + width/2) * image.shape[1])
        y_max = int((y_center + height/2) * image.shape[0])
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 5)

        # Add class name to the bounding box
        class_name = class_names.get(int(class_id), "Unknown")
        cv2.putText(image, class_name, (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the image with bounding boxes
    axs[row, col].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axs[row, col].axis('off')

    # Display the image dimensions and channels
    h, w, c = image.shape
    axs[row, col].set_title(f"{w}x{h}, {c} channels")

from glob import glob
import os
import shutil

def make_directory(source_folder, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    files = glob(f"{source_folder}/*")
    for file in files:
        if os.path.isdir(file):
            shutil.copytree(file, os.path.join(destination_folder, os.path.basename(file)))
        elif os.path.isfile(file):
            shutil.copy(file, destination_folder)

source_folder = "C:\\Users\\Administrator\\PyCharmMiscProject\\j\\train"
destination_folder = "C:\\Users\\Administrator\\PyCharmMiscProject\\ouput"

make_directory(source_folder, destination_folder)
print("Folder structure created successfully!")

model = YOLO('yolov8n.pt')

# Train the model with your custom file
results = model.train(
    data='C:\\Users\\Administrator\\PyCharmMiscProject\\j\\data.yaml',
    epochs=100,
    imgsz=416,
    device='cpu',
    patience=50,
    batch=32,
    optimizer='auto',
    lr0=0.0001,
    lrf=0.1,
    seed=0,
    dropout=0.2,
    plots=True)