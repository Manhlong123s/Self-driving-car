import os
import unicodedata

# Đường dẫn thư mục chứa các file ảnh
folder_path = "C:\\Users\\Administrator\\PyCharmMiscProject\\biển báo cấm"  # Thay thế bằng đường dẫn thư mục của bạn

# Kiểm tra nếu thư mục tồn tại
if not os.path.exists(folder_path):
    print("Thư mục không tồn tại.")
    exit()

# Lấy tất cả các file trong thư mục
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)]

# Kiểm tra nếu không có file ảnh
if not image_files:
    print("Không tìm thấy ảnh trong thư mục.")
    exit()


# Hàm chuyển tên file về dạng không dấu và thêm dấu gạch dưới giữa các từ
def clean_filename(filename):
    # Bỏ dấu tiếng Việt
    name_no_accent = ''.join(
        c for c in unicodedata.normalize('NFKD', filename) if not unicodedata.combining(c)
    )
    # Thêm dấu gạch dưới giữa các từ
    clean_name = name_no_accent.replace(" ", "_").lower()
    return clean_name


# Duyệt qua các file ảnh và đổi tên
for file_name in image_files:
    # Lấy đường dẫn đầy đủ của file
    file_path = os.path.join(folder_path, file_name)

    # Tách tên file và phần mở rộng
    name, ext = os.path.splitext(file_name)

    # Lấy tên file đã chỉnh sửa
    new_name = clean_filename(name) + ext

    # Tạo đường dẫn mới
    new_file_path = os.path.join(folder_path, new_name)

    # Đổi tên file
    os.rename(file_path, new_file_path)
    print(f"Đổi tên: {file_name} -> {new_name}")
