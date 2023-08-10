import random
# from math import ceil
import hashlib
from decimal import Decimal
from itertools import combinations


FIELD_SIZE = 10**5
# webserver的标记
server_name_list = ['Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5']


def reconstruct_secret(shares):
    """
    Combines individual shares (points on graph)
    using Lagranges interpolation.

    `shares` is a list of points (x, y) belonging to a
    polynomial with a constant of our key.
    """
    sums = 0
    prod_arr = []

    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))

        prod *= yj
        sums += Decimal(prod)

    return int(round(Decimal(sums), 0))

def polynom(x, coefficients):
    """
    This generates a single point on the graph of given polynomial
    in `x`. The polynomial is given by the list of `coefficients`.
    """
    point = 0
    # Loop through reversed list, so that indices from enumerate match the
    # actual coefficient indices
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point

def coeff(t, secret):
    """
    Randomly generate a list of coefficients for a polynomial with
    degree of `t` - 1, whose constant is `secret`.

    For example with a 3rd degree coefficient like this:
        3x^3 + 4x^2 + 18x + 554

        554 is the secret, and the polynomial degree + 1 is
        how many points are needed to recover this secret.
        (in this case it's 4 points).
    """
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff

def generate_shares(n, m, secret):
    """
    Split given `secret` into `n` shares with minimum threshold
    of `m` shares to recover this `secret`, using SSS algorithm.
    """
    coefficients = coeff(m, secret)
    shares = []

    for i in range(1, n+1):
        x = random.randrange(1, FIELD_SIZE)
        shares.append((x, polynom(x, coefficients)))

    return shares


# 我们这里获取
def generate_webserver_shares(n, t, org_password):
    new_org_password = []
    for item in org_password:
        temp_password_ss = generate_shares(n, t, item)
        new_org_password.append(temp_password_ss)
    # print(new_org_password)

    webserver_ss_list = [list(row) for row in zip(*new_org_password)]
    for index in range(n):
        hash_object = hashlib.md5()
        hash_object.update(server_name_list[index].encode('unicode-escape'))
        hash_value = hash_object.hexdigest()
        decimal_value = int(hash_value, 16)
        webserver_ss_list[index].append((random.randrange(1, FIELD_SIZE), decimal_value))
    print(len(webserver_ss_list), len(webserver_ss_list[0]))
    # print(webserver_ss_list)

    return webserver_ss_list


# 随机抽取三台服务器上的秘密份额
def reconstruct_webserver_secret(webserver_ss_list, random_sequence):
    reveal_list = [webserver_ss_list[i] for i in random_sequence]
    # reveal_list = random.sample(webserver_ss_list, 3)
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
        temp_password = reconstruct_secret(item)
        result.append(temp_password)

    # 返回password编码后的list
    return result


# 自我检查模块
def webserver_selfcheck(n, t, webserver_ss_list, org_password):
    # 开始自我检查
    # 首先获取3个元素的全部排列可能
    my_list = list(range(n))
    permutations = list(combinations(my_list, t))
    print(permutations)
    # 可成功配对的3个元素的组合
    success_tuple = ()
    for test in permutations:
        check_seq = list(test)
        temp = reconstruct_webserver_secret(webserver_ss_list, check_seq)
        if temp == org_password:
            success_tuple = test
            break
        else:
            continue
    # 如果没有成功恢复的，给出警告信息
    if not success_tuple:
        print('Warning, too many Hijacked server!!!')
        exit(0)  # 直接退出程序
    else:
        print('Get the success tuple: ', success_tuple)
    values_to_remove = list(success_tuple)
    rest_nodelist_tocheck = [x for x in my_list if x not in values_to_remove]
    print('the rest node to check: ', rest_nodelist_tocheck)

    # 开始逐一检查
    detect_Hijacked_nodelist = []
    for node in rest_nodelist_tocheck:
        base_list = list(success_tuple)[:-1]
        print('the base node list: ', base_list)
        base_list.append(node)
        # 开始恢复secret
        temp = reconstruct_webserver_secret(webserver_ss_list, base_list)
        if temp == org_password:
            print('node ', node, ' Not Hijacked')
        else:
            detect_Hijacked_nodelist.append(node)
            print('node ', node, ' Hijacked!!!')

    return detect_Hijacked_nodelist


# Driver code
if __name__ == '__main__':
    print('-----------------------------------------------------------\n\n')
    # (3,5) sharing scheme
    t, n = 3, 5
    secret = 12345678
    print(f'Original Secret: {secret}')

    # Phase I: Generation of shares
    shares = generate_shares(n, t, secret)
    print(f'Shares: {", ".join(str(share) for share in shares)}')

    # Phase II: Secret Reconstruction
    # Picking t shares randomly for
    # reconstruction
    pool = random.sample(shares, t)
    print(f'Combining shares: {", ".join(str(share) for share in pool)}')
    print(f'Reconstructed secret: {reconstruct_secret(pool)}')
    print('-----------------------------------------------------------\n\n')


    # 现在加入类似于hash的node节点标记
    org_password = [102, 122, 107, 49, 50, 51, 52, 53, 54, 78, 102, 1234]
    print('org_password: ', org_password)
    webserver_ss_list = generate_webserver_shares(n, t, org_password)

    # 随机抽取三份来做秘密重构[1, 2, 3]
    random_sequence = random.sample(range(n), t)
    print('random sequence: ', random_sequence)
    reveal_password = reconstruct_webserver_secret(webserver_ss_list, random_sequence)
    print('the reveal password: ', reveal_password)
    print('-----------------------------------------------------------\n\n')



    '''
    我们在这里进行自检模块的模拟
    随机选取5台服务器中的1-2台作为被劫持的服务器
    '''
    # random_Hijacked = random.randint(0, 4)
    random_Hijacked = [0, 1]
    print('Hijacked: ', random_Hijacked)

    # 修改对应节点的数值，对其+1，来模拟被劫持节点
    for node in random_Hijacked:
        # print('org node', node, 'data: ', webserver_ss_list[node])
        Hijacked_list = []
        for item in webserver_ss_list[node]:
            new_list = list(item)
            new_list[1] = new_list[1] + 1
            new_tuple = tuple(new_list)
            Hijacked_list.append(new_tuple)
        # print('Hijacked node' , node, 'data: ', Hijacked_list)
        webserver_ss_list[node] = Hijacked_list

    reveal_seq = [0, 1, 2]
    test_password = reconstruct_webserver_secret(webserver_ss_list, reveal_seq)
    # 测试输出错误信息
    if test_password == org_password:
        print('Successfully verified!!!')
    else:
        print('error password: ', test_password)

    detect_result = webserver_selfcheck(n, t, webserver_ss_list, org_password)
    print('All the Hijacked Node: ', detect_result)




    '''
    这一部分就是用来测试hashlib的
    '''
    print('-----------------------------------------------------------\n\n')
    a = 'webserver1'
    b = 'webserver2'
    hash_object = hashlib.md5()
    # 更新哈希对象的输入
    hash_object.update(a.encode('unicode-escape'))
    # 计算哈希值
    hash_value = hash_object.hexdigest()
    decimal_value = int(hash_value, 16)
    print(hash_value, decimal_value)

    hash_object.update(b.encode('unicode-escape'))
    hash_value = hash_object.hexdigest()
    decimal_value = int(hash_value, 16)
    print(hash_value, decimal_value)

