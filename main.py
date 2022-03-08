import math
import random

M = 32
Q = 32
aprox_F_m = 0.2888
aprox_F_m1 = 0.5776
aprox_remains = 0.1336
threshold = 0.01


def find_row(start_index, end_index, matrix):
    step = 1 if start_index <= end_index else -1
    for i in range(start_index + step, end_index, step):
        if matrix[i][start_index] == 1:
            return i
    return -1


def binary_matrix_rank(matrix):
    # Forward row operations
    for i in range(len(matrix) - 1):  # step 1 & 4
        if matrix[i][i] != 1:  # step 2
            swap_row = find_row(i, len(matrix), matrix)
            if swap_row > i:
                aux = matrix[i]
                matrix[i] = matrix[swap_row]
                matrix[swap_row] = aux
        if matrix[i][i] == 1:  # step 3
            for next_row in range(i + 1, len(matrix)):  # step 3a & 3g & 3h
                if matrix[next_row][i] != 0:  # step 3c
                    for col in range(i, len(matrix[next_row])):  # step 3b & 3e & 3f
                        matrix[next_row][col] = matrix[next_row][col] ^ matrix[i][col]  # step 3d

    # Backward row operation
    for i in range(len(matrix) - 1, 0, -1):  # step 1 & 4
        if matrix[i][i] != 1:  # step 2
            swap_row = find_row(i, -1, matrix)
            if i > swap_row > -1:
                aux = matrix[i]
                matrix[i] = matrix[swap_row]
                matrix[swap_row] = aux
        if matrix[i][i] == 1:  # step 3
            for next_row in range(i - 1, -1, -1):  # step 3a & 3g & 3h
                if matrix[next_row][i] != 0:  # step 3c
                    for col in range(i, len(matrix[next_row])):  # step 3b & 3e & 3f
                        matrix[next_row][col] = matrix[next_row][col] ^ matrix[i][col]  # step 3d

    rank = 0
    for line in matrix:
        if 1 in line:
            rank = rank + 1
    return rank


def bitfield(bits_string):
    return [int(bit) for bit in bits_string.replace(' ', '')]


def build_matrix_list(eps):
    n = len(eps)
    N = math.floor(n / (M * Q))
    # print(f"n = {n}")
    # print(f"N = {N}, M = {M}, Q = {Q}")

    matrix_list = []
    for index in range(N):
        tmp_matrix = []
        for row_index in range(M):  # '010 110 010 010 101 011 01'
            start_point = row_index * Q + index * M * Q  # 036 9
            tmp_matrix.append(eps[start_point:start_point + Q])
        matrix_list.append(tmp_matrix)
        # for i in tmp_matrix:
        #     print(i)
        # print("-" * 50)
    return matrix_list


def binary_matrix_rank_test(input_string: str):
    bit_list = bitfield(input_string)
    # print(f"input = {bit_list}")
    matrix_list = build_matrix_list(bit_list)  # step (1)
    matrix_rank_list = []
    F_m = 0  # matrix with max_rank
    F_m1 = 0  # matrix with max_rank - 1
    F_remaining = 0  # matrix with max_rank

    for matrix in matrix_list:
        rank = binary_matrix_rank(matrix)  # step (2)
        if rank == M:  # step (3)
            F_m += 1
        elif rank == M - 1:
            F_m1 += 1
        else:
            F_remaining += 1
        matrix_rank_list.append(rank)

    # print(matrix_rank_list)
    # print(f"F_m = {F_m}, F_m-1 = {F_m1}, N - F_m - F_m-1 = {F_remaining}")

    N = math.floor(len(bit_list) / (M * Q))  # step (4)
    square_x = ((F_m - aprox_F_m * N) ** 2) / (aprox_F_m * N)
    square_x += ((F_m1 - aprox_F_m1 * N) ** 2) / (aprox_F_m1 * N)
    square_x += ((F_remaining - aprox_remains * N) ** 2) / (aprox_remains * N)
    # print(f"square_x = {square_x}")

    P_val = math.e ** ((-square_x) / 2)  # step (5)
    # print(f"P-value = {P_val}")
    if P_val < threshold:
        # print("Sequence is NON-random")
        return False, P_val
    # print("Sequence is random")
    return True, P_val


def test():
    count_bits = 100000
    count_random = 0
    count_non_random = 0
    file = open("stat2.txt", "a")
    for density in range(count_bits):
        eps = ''
        count = 0
        for _ in range(count_bits):
            bit = random.randint(0, 1)
            if count < density:
                eps += str(bit)
                if bit == 1:
                    count += 1
            else:
                eps += '0'

        is_random, p_val = binary_matrix_rank_test(eps)
        if is_random:
            count_random += 1
        else:
            count_non_random += 1
        print("===", density, count, is_random)
        file.write(f"{count};{count_bits};{str(p_val).replace('.', ',')}\n")
    file.close()
    print(f"Random sequence = {count_random}")
    print(f"NON-Random sequence = {count_non_random}")


if __name__ == '__main__':
    test()
    quit()
    # bit_list = bitfield('01011001001010101101')
    count_non_random = 0
    count_random = 0
    test_count = 1000
    count_bits = 100000
    density = 0
    file = open("stat.txt", "a")
    for i in range(test_count):
        density = 0
        eps = ''
        for _ in range(count_bits):
            bit = random.randint(0, 1)
            density += bit
            eps += str(bit)
        # print("eps =", eps)

        is_random, p_val = binary_matrix_rank_test(eps)
        if is_random:
            count_random += 1
        else:
            count_non_random += 1
        file.write(f"{density};{count_bits};{str(p_val).replace('.', ',')}\n")
        print("===", i + 1, "-" * 50)
    file.close()
    print(f"Random sequence = {count_random}")
    print(f"NON-Random sequence = {count_non_random}")

    # eps = "000001001011" + "0"*100000
    # binary_matrix_rank_test(eps)

    # M = [bitfield('1 0 0 0 0 0'),
    #      bitfield('0 0 0 0 0 1'),
    #      bitfield('1 0 0 0 0 1'),
    #      bitfield('1 0 1 0 1 0'),
    #      bitfield('0 0 1 0 1 1'),
    #      bitfield('0 0 0 0 1 0')]
