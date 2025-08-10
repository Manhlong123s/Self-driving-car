import os
import cv2
import unicodedata
import re
import albumentations as A
# Thiết lập thư mục đích
destination_root = "C:\\Users\\FPT\\PyCharmMiscProject\\augemt"  # Đổi thành thư mục đích của bạn
os.makedirs(destination_root, exist_ok=True)

# Đường dẫn tới thư mục chứa ảnh
folder_path = "C:\\Users\\FPT\\PyCharmMiscProject\\data"  # Đổi thành thư mục chứa ảnh của bạn

# Kiểm tra nếu không có thư mục nào được chỉ định
if not folder_path:
    print("No folder was selected.")
    exit()

# Lấy danh sách tất cả các tệp ảnh trong thư mục
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]

# Kiểm tra nếu không có ảnh trong thư mục
if not image_files:
    print("No images found in the selected folder.")
    exit()

# --- Danh sách các phép biến đổi (augmentations) ---
augmentations = {
    'rotate_30': A.Rotate(limit=30, p=1),
    'rotate_60': A.Rotate(limit=60, p=1),
    'rotate_90': A.Rotate(limit=90, p=1),
    'rotate_120': A.Rotate(limit=120, p=1),
    'rotate_150': A.Rotate(limit=150, p=1),
    'rotate_180': A.Rotate(limit=180, p=1),
    'flip_horizontal': A.HorizontalFlip(p=1),
    'flip_vertical': A.VerticalFlip(p=1),
    'random_crop': A.RandomCrop(height=200, width=200, p=1),
    'random_brightness': A.RandomBrightnessContrast(p=1),
    'blur': A.Blur(blur_limit=50, p=1),
    'GaussianBlur': A.GaussianBlur(blur_limit=(3, 7), p=1),
    'MedianBlur': A.MedianBlur(blur_limit=(3, 7), p=1),
    'MotionBlur': A.MotionBlur(blur_limit=(3, 7), p=1),
    'contrast1': A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1.0),
    'Hue': A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=1.0),
    'channel Shuffle': A.ChannelShuffle(p=1),
    'Histogram Equalization': A.CLAHE(clip_limit=4.0, tile_grid_size=(8, 8), p=1.0),
    'Posterize': A.Posterize(num_bits=4, p=1.0),
    'shift_scale_rotate': A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=20, p=1),
    'elastic_transform': A.ElasticTransform(p=1),
    'grid_distortion': A.GridDistortion(p=1),
    'Affine Transform': A.Affine(scale=(0.9, 1.1), translate_percent=(0.1, 0.1), rotate=(-20, 20), shear=(-10, 10),
                                 p=1.0),
    'Perspective Transform': A.Perspective(scale=(0.05, 0.1), p=1.0),
}

# Duyệt qua tất cả các ảnh trong thư mục và áp dụng các phép biến đổi
for file_name in image_files:
    # Đọc ảnh
    file_path = os.path.join(folder_path, file_name)

    # Đảm bảo đường dẫn đúng Unicode
    try:
        image_cv = cv2.imread(file_path)
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        continue

    if image_cv is None:
        print(f"Unable to read the image from: {file_path}")
        continue

    # Làm sạch tên tệp và tạo thư mục đích
    name, ext = os.path.splitext(file_name)

    # Loại bỏ dấu ngoặc và nội dung bên trong tên file
    clean_name = re.sub(r'\(.*?\)', '', name).strip().replace(' ', '_')
    clean_name = ''.join(c for c in unicodedata.normalize('NFKD', clean_name) if not unicodedata.combining(c))
    clean_name = clean_name.lower()

    target_folder = os.path.join(destination_root, clean_name)
    os.makedirs(target_folder, exist_ok=True)

    # Tạo log tệp đã lưu
    log_file = os.path.join(target_folder, "saved_filenames.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(file_name + "\n")

    # Áp dụng các phép biến đổi và lưu kết quả
    for name, aug in augmentations.items():
        augmented = aug(image=cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))
        aug_image = augmented['image']
        aug_image_bgr = cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR)
        output_path = os.path.join(target_folder, f"{name}_{file_name}")
        cv2.imwrite(output_path, aug_image_bgr)
        print(f"Saved: {output_path}")
