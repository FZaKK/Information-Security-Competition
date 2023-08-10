import numpy as np
import random
from itertools import combinations
import hashlib


FIELD_SIZE = 10**5
# webserver的标记
server_name_list = ['Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5']
# 预定的规则
rules = [(1, 5), (2, 3, 4)]
# 向量维度
vec_dim = 3
# 目标向量
target_vector = np.array([1, 0, 0])


def coeff(t, secret):
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeff.insert(0, secret)
    return coeff

# 这里我肯定是需要一个judge判断函数，将规则内与规则外分开判断
def vector_judge(rules, server_vector):
    num = len(server_name_list)
    number_list = list(range(1, num + 1))
    lengths = number_list[1:]
    # 这里获得所有可能的排列也就是规则
    combinations_list = []
    for length in lengths:
        combs = combinations(number_list, length)
        combinations_list.extend(list(combs))
    print(len(combinations_list))
    # print(combinations_list)

    # 单独把规则内和规则外隔开，此时的combination_list就是规则之外了
    for rule in rules:
        combinations_list.remove(rule)
    print(len(combinations_list))

# Brickell方案主要的难点就是生成向量
def gen_vector(rules):
    server_vector = np.zeros((len(server_name_list), vec_dim))
    low_value = -2
    high_value = 2
    for rule in rules:
        print(rule)
        if len(rule) == 2:
            temp_vector = []
            vector1 = np.random.randint(low_value, high_value, size=3)
            vector2 = np.array([1, 0, 0], dtype=int) - vector1
            print(vector1, vector2)
            temp_vector.append(vector1)
            temp_vector.append(vector2)
            for index in range(len(rule)):
                server_vector[rule[index] - 1] = temp_vector[index]
        if len(rule) == 3:
            temp_vector = []
            vector1 = np.random.randint(low_value, high_value, size=3)
            vector2 = np.random.randint(low_value, high_value, size=3)
            vector3 = np.array([1, 0, 0], dtype=int) - vector1 - vector2
            print(vector1, vector2, vector3)
            temp_vector.append(vector1)
            temp_vector.append(vector2)
            temp_vector.append(vector3)
            for index in range(len(rule)):
                server_vector[rule[index] - 1] = temp_vector[index]
        if len(rule) == 4:
            print('Please increase the vec dim!!!')
            return np.zeros((len(server_name_list), vec_dim))
        if len(rule) == 1 or len(rule) == 5:
            print('Error rules!!!')
            return np.zeros((len(server_name_list), vec_dim))

    return server_vector

# 进行秘密份额的划分
def generate_shares(secret, server_vector):
    vec_coeff = coeff(t, secret)
    vec_coeff_mat = np.array(vec_coeff)
    shares = []
    for vec in server_vector:
        shares.append(np.dot(vec_coeff_mat, vec))

    return shares

# 重构秘密
def reconstruct_secret(serials, shares, server_vector):
    server_vector_reveal = server_vector[serials]
    reveal_vec = []
    for vec in server_vector_reveal:
        reveal_vec.append(vec)
    coeff_matrix = np.vstack(tuple(reveal_vec)).T
    # coefficients = np.linalg.solve(coeff_matrix, target_vector)
    coefficients = [1] * len(serials)
    # print(coefficients)

    selected_shares = [shares[i] for i in serials]

    return int(np.dot(coefficients, selected_shares))

# web部分的生成秘密份额
def generate_webserver_shares(webserver_vector, org_password):
    new_org_password = []
    for item in org_password:
        temp_password_ss = generate_shares(item, webserver_vector)
        new_org_password.append(temp_password_ss)
    print(new_org_password)

    webserver_ss_list = [list(row) for row in zip(*new_org_password)]
    for index in range(len(server_name_list)):
        hash_object = hashlib.md5()
        hash_object.update(server_name_list[index].encode('unicode-escape'))
        hash_value = hash_object.hexdigest()
        decimal_value = int(hash_value, 16)
        # webserver_ss_list[index].append((random.randrange(1, FIELD_SIZE), decimal_value))
        webserver_ss_list[index].append(decimal_value)
    print(len(webserver_ss_list), len(webserver_ss_list[0]))
    # print(webserver_ss_list)

    return webserver_ss_list

# web部分重构秘密
def reconstruct_webserver_secret(webserver_ss_list, reveal_sequence, server_vector):
    reveal_list = webserver_ss_list
    # reveal_list = [webserver_ss_list[i] for i in reveal_sequence]
    # print(len(reveal_list), len(reveal_list[0]))

    # 重构秘密
    # print(reveal_list)
    # 去除hash标记进行重构，这个东西要不要shuffle，短暂的来说先不shuffle了
    for index in range(t):
        reveal_list[index] = reveal_list[index][:-1]
    reveal_list = [list(row) for row in zip(*reveal_list)]
    # print(reveal_list)
    # print(len(reveal_list), len(reveal_list[0]))
    result = []
    for item in reveal_list:
        temp_password = reconstruct_secret(reveal_sequence, item, server_vector)
        result.append(temp_password)

    # 返回password编码后的list
    return result


if __name__ == '__main__':
    t, n = 3, 5
    secret = 1234
    vec_coeff = coeff(t, secret)
    print(vec_coeff)
    webserver_vector = gen_vector(rules)
    # 转换为int类型矩阵
    webserver_vector = webserver_vector.astype(int)
    print(webserver_vector)

    # 秘密分割与重构
    secret_shares = generate_shares(secret, webserver_vector)
    print(secret_shares)
    # 重构时假设收回的节点编号是[1, 2, 3]，0和4未收回
    server_reveal = [1, 2, 3]
    print(reconstruct_secret(server_reveal, secret_shares, webserver_vector))



    # 这里模拟一下web中真实的密码
    org_password = [102, 122, 107, 49, 50, 51, 52, 53, 54, 78, 102, 1234]
    print('org_password: ', org_password)
    webserver_ss_list = generate_webserver_shares(webserver_vector, org_password)
    # web重构
    reveal_sequence = [1, 2, 3]
    reveal_password = reconstruct_webserver_secret(webserver_ss_list, reveal_sequence, webserver_vector)
    print('the reveal password: ', reveal_password)
