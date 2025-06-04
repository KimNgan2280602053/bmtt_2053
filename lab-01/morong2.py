import re

# Nhập chuỗi
chuoi = input("Nhập chuỗi chứa số nguyên: ")

# Tìm tất cả số nguyên (âm hoặc dương)
so_nguyen = re.findall(r'-?\d+', chuoi)

# Chuyển thành số nguyên
so_nguyen = [int(x) for x in so_nguyen]

# Tổng giá trị âm
tong_am = sum(x for x in so_nguyen if x < 0)

# Tổng giá trị dương (gồm cả trị tuyệt đối số âm)
tong_duong = sum(abs(x) for x in so_nguyen if x > 0 or x < 0)

# In kết quả
print("Giá trị dương:", tong_duong)
print("Giá trị âm:", tong_am)
