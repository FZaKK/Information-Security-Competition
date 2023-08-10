# Additive Sharing with facility to Refresh shares via Proactivization
import random
import hashlib
import copy


FIELD_SIZE = 10**16
server_name_list = ['Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5']


def getAdditiveShares(secret, N, fieldSize):
    '''Generate N additive shares from 'secret' in finite field of size 'fieldSize'.'''

    # Generate n-1 shares randomly
    shares = [random.randrange(fieldSize) for i in range(N-1)]
    # Append final share by subtracting all shares from secret
    shares.append((secret - sum(shares)) % fieldSize )
    return shares


def reconstructSecret(shares, fieldSize):
    '''Regenerate secret from additive shares'''
    return sum(shares) % fieldSize


def proactivizeShares(shares):
    '''Refreshed shares by proactivization'''

    n = len(shares)
    refreshedShares = [0]*n

    for s in shares:

        # Divide each share into sub-fragments using additive sharing
        subShares = getAdditiveShares(s, n, FIELD_SIZE)

        # Add subfragments of corresponding parties
        for p, sub in enumerate(subShares):
            refreshedShares[p] += sub

    return refreshedShares


# 获取webserver各个服务器的分片
# def generate_webserver_shares(n, t, org_password):
def generate_webserver_shares(n, org_password):
    webserver_ss_list = [getAdditiveShares(x, n, FIELD_SIZE) for x in org_password]
    # print(webserver_ss_list)
    print(len(webserver_ss_list), len(webserver_ss_list[0]))

    webserver_ss_list = [list(row) for row in zip(*webserver_ss_list)]
    print(len(webserver_ss_list), len(webserver_ss_list[0]))

    # compute the hash
    for index in range(n):
        hash_object = hashlib.md5()
        hash_object.update(server_name_list[index].encode('unicode-escape'))
        hash_value = hash_object.hexdigest()
        decimal_value = int(hash_value, 16)
        webserver_ss_list[index].append(decimal_value)
    # print(webserver_ss_list)
    print(len(webserver_ss_list), len(webserver_ss_list[0]))

    return webserver_ss_list


# 重构secret
def reconstruct_webserver_secret(reveal_list, FIELD_SIZE):
    for index in range(n):
        reveal_list[index] = reveal_list[index][:-1]
    reveal_list = [list(row) for row in zip(*reveal_list)]

    result = []
    for item in reveal_list:
        temp_password = reconstructSecret(item, fieldSize=FIELD_SIZE)
        result.append(temp_password)

    return result


# 更新webserver的秘密份额
def refresh_webserver_secret(webserver_ss_list):
    print(webserver_ss_list)

    hash_list = []
    for ss_list in webserver_ss_list:
        hash_value = ss_list.pop()
        hash_list.append(hash_value)
    print(len(webserver_ss_list), len(webserver_ss_list[0]))
    # print(hash_list)

    # refresh the data element
    webserver_ss_list = [list(row) for row in zip(*webserver_ss_list)]
    print(len(webserver_ss_list), len(webserver_ss_list[0]))
    for index in range(len(webserver_ss_list)):
        webserver_ss_list[index] = proactivizeShares(webserver_ss_list[index])

    webserver_ss_list = [list(row) for row in zip(*webserver_ss_list)]
    print(len(webserver_ss_list), len(webserver_ss_list[0]))
    for index in range(len(webserver_ss_list)):
        webserver_ss_list[index].append(hash_list[index])
    print(webserver_ss_list)
    print(len(webserver_ss_list), len(webserver_ss_list[0]))

    return webserver_ss_list



if __name__ == "__main__":
    print('-----------------------------------------------------------\n\n')
    # Generating the shares
    # params: secret, participants num, field
    n = 5
    shares = getAdditiveShares(1234, n, FIELD_SIZE)
    print('Shares are:', shares)

    # Running Proactivization
    newShares = proactivizeShares(shares)
    print('Refreshed Shares are:', newShares)

    # Reconstructing secret from refreshed shares
    print('Secret:', reconstructSecret(newShares, FIELD_SIZE))
    print('-----------------------------------------------------------\n\n')

    # simulate the reality password
    org_password = [102, 122, 107, 49, 50, 51, 52, 53, 54, 78, 102, 1234]
    print(org_password)
    webserver_ss_list = generate_webserver_shares(n, org_password)

    # 重构secret
    reveal_list = copy.deepcopy(webserver_ss_list)
    result = reconstruct_webserver_secret(reveal_list, FIELD_SIZE)
    print(result)

    # refresh一下后，重构秘密份额
    webserver_ss_list = refresh_webserver_secret(webserver_ss_list)
    new_reveal_list = copy.deepcopy(webserver_ss_list)
    new_result = reconstruct_webserver_secret(new_reveal_list, FIELD_SIZE)
    print(new_result)
