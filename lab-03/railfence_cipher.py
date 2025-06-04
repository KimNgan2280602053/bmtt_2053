class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails <= 1 or num_rails >= len(plain_text):
            return plain_text

        rails = ['' for _ in range(num_rails)]
        row = 0
        direction = 1  # 1: xuống, -1: lên

        for char in plain_text:
            rails[row] += char
            if row == 0:
                direction = 1
            elif row == num_rails - 1:
                direction = -1
            row += direction

        return ''.join(rails)

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if num_rails <= 1 or num_rails >= len(cipher_text):
            return cipher_text

        pattern = [0] * len(cipher_text)
        row = 0
        direction = 1

        for i in range(len(cipher_text)):
            pattern[i] = row
            if row == 0:
                direction = 1
            elif row == num_rails - 1:
                direction = -1
            row += direction

        rail_counts = [pattern.count(r) for r in range(num_rails)]
        rails = []
        idx = 0
        for count in rail_counts:
            rails.append(list(cipher_text[idx:idx + count]))
            idx += count

        result = ''
        rail_indices = [0] * num_rails
        for r in pattern:
            result += rails[r][rail_indices[r]]
            rail_indices[r] += 1

        return result
