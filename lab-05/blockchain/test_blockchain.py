from blockchain import Blockchain

# Tạo blockchain mới
my_blockchain = Blockchain()

# Thêm một số giao dịch
my_blockchain.add_transaction('Alice', 'Bob', 10)
my_blockchain.add_transaction('Bob', 'Charlie', 5)
my_blockchain.add_transaction('Charlie', 'Alice', 3)

# Lấy block trước và proof của nó
previous_block = my_blockchain.get_previous_block()
previous_proof = previous_block.proof

# Tìm proof mới
new_proof = my_blockchain.proof_of_work(previous_proof)

# Lấy hash của block trước
previous_hash = previous_block.hash

# Thêm phần thưởng khối (giống như Bitcoin)
my_blockchain.add_transaction('Genesis', 'Miner', 1)

# Tạo block mới
new_block = my_blockchain.create_block(new_proof, previous_hash)

# In toàn bộ blockchain
for block in my_blockchain.chain:
    print(f"Block {block.index}:")
    print(f"  Previous Hash: {block.previous_hash}")
    print(f"  Timestamp: {block.timestamp}")
    print(f"  Transactions: {block.transactions}")
    print(f"  Proof: {block.proof}")
    print(f"  Hash: {block.hash}\n")

# Kiểm tra tính hợp lệ của chuỗi
print("Blockchain is valid:", my_blockchain.is_chain_valid(my_blockchain.chain))
