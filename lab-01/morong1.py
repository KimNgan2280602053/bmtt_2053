import itertools

# Danh sách ban đầu
data = [1, 2, 3]

# Tạo hoán vị
permutations = list(itertools.permutations(data))

# In kết quả
print("Tất cả các hoán vị của [1, 2, 3]:")
for p in permutations:
    print(p)
