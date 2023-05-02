# GROUP MEMBERS: BSEF20A003, BSEF20A006, BSEF20A028, BSEF20A047
#s-des Implementation

P10 = ['3', '5', '2', '7', '4', '10', '1', '9', '8', '6']
P8 = ['6', '3', '7', '4', '8', '5', '10', '9']
P4 = ['2', '4', '3', '1']

IP = ['2', '6', '3', '1', '4', '8', '5', '7']
IPInv = ['4', '1', '3', '5', '7', '2', '8', '6']
EP = ['4', '1', '2', '3', '2', '3', '4', '1']

S0 = [
    ['01', '00', '11', '10'],
    ['11', '10', '01', '00'],
    ['00', '10', '01', '11'],
    ['11', '01', '11', '10']
]

S1 = [
    ['00', '01', '10', '11'],
    ['10', '00', '01', '11'],
    ['11', '00', '01', '00'],
    ['10', '01', '00', '11']
]

def p10(str):
    answer = ''
    for i in P10:
        answer += str[int(i) - 1]
    return answer

def p8(str):
    answer = ''
    for i in P8:
        answer += str[int(i) - 1]
    return answer

def p4(str):
    answer = ''
    for i in P4:
        answer += str[int(i) - 1]
    return answer

def ls1(str):
    first = str[0]
    str = str[1:]
    str = str + first
    return str

def ls2(str):
    firstTwo = str[0:2]
    str = str[2:]
    str = str + firstTwo
    return str

def ip(str):
    answer = ''
    for i in IP:
        answer += str[int(i) - 1]
    return answer

def ipInv(str):
    answer = ''
    for i in IPInv:
        answer += str[int(i) - 1]
    return answer

def ep(str):
    answer = ''
    for i in EP:
        answer += str[int(i) - 1]
    return answer

def xor(str, key):
    answer = ''
    for i in range(0, len(str)):
        if str[i] == key[i]:
            answer += '0'
        else:
            answer += '1'

    return answer

def sbox_operation(val, sbox):
    row = int(val[0]+val[3],2)
    col = int(val[1]+val[2],2)

    return sbox[row][col]

def keys_generation():
    while (True):
        try:
            tenBitKey = input('\nEnter a 10 bit key: ')
            for i in tenBitKey:
                if i != '0' and i != '1':
                    raise Exception('ERROR: You entered an invalid key! key can only have 0 and 1')

            if len(tenBitKey) != 10:
                raise Exception('ERROR: Length of key can only be 10 bits')
            break
        except Exception as e:
            print(e)

    p10_key = p10(tenBitKey)  #P10 operation on the Key
    leftHalf = p10_key[0: len(p10_key)//2]  #Left Half of Key After P10  
    rightHalf = p10_key[len(p10_key)//2:]   #Right Half of Key After P10

    leftHalf_ls1 = ls1(leftHalf) #LS1 on Left Half
    rightHalf_ls1 = ls1(rightHalf) #LS1 on Right Half

    str = leftHalf_ls1 + rightHalf_ls1 #Combining Left & Right Half of Key After LS1 operation on Both Halves
    key1 = p8(str) # P8 Operation on the result to Get First Key

    leftHalf_ls2 = ls2(leftHalf_ls1) #LS2 on the Left Half After LS1
    rightHalf_ls2 = ls2(rightHalf_ls1) #LS2 on the Right Half After LS1

    str = leftHalf_ls2 + rightHalf_ls2 #Combining Left & Right Half of Key After LS2 operation on Both Halves
    key2 = p8(str) # P8 Operation on the result to Get Second Key

    return {'key1': key1, 'key2': key2}

def round(txt, key):
    left_half_for_xor = txt[0: len(txt) // 2]
    right_half = txt[len(txt) // 2:]

    # applying EP on right half of IP or switch
    right_half_ep = ep(right_half)

    # xor EP text with key(1 or 2)
    right_half_ep_xored = xor(right_half_ep, key)

    # halves
    L_right_half_ep_xored = right_half_ep_xored[0: len(right_half_ep_xored) // 2]  # get left half for applying substitution box S0
    R_right_half_ep_xored = right_half_ep_xored[len(right_half_ep_xored) // 2:]  # get right half for applying substitution box S1

    # substitution boxes
    left_half = sbox_operation(L_right_half_ep_xored, S0)  # applying S0 sbox on left half of xor
    right_half = sbox_operation(R_right_half_ep_xored, S1)  # applying S1 sbox on right half of xor

    # combining
    str = left_half + right_half  # combining for P4

    # applying P4
    str_p4 = p4(str)
    # XOR P4 text with left half of text for later(IP or switch)
    str_p4_xored = xor(str_p4, left_half_for_xor)
    return str_p4_xored

def encrypt(plain_text, key1, key2):
    txt = ip(plain_text)
    right_half = txt[len(txt) // 2:]  # get right half for switch later

    #round1
    round1_val = round(txt, key1)

    #switch xor of first round and right_half of ip
    txt = right_half + round1_val
    right_half = txt[len(txt) // 2:]  # get right half for IP-1 later

    #round2
    round2_val = round(txt, key2)

    txt = round2_val + right_half
    txt = ipInv(txt)
    return txt

bool = True
keys = keys_generation()

while (True):
        try:
            pt = input('\nEnter 8 bit Plain Text: ')
            for i in pt:
                if i != '0' and i != '1':
                    raise Exception('ERROR: Plain Text can only be Binary i.e. 0 & 1')

            if len(pt) != 8:
                raise Exception('ERROR: Length of Plain Text can only be 8 bits')
            break
        except Exception as e:
            print(e)

k1=keys["key1"]
k2=keys["key2"]

print("\nEncryption in Progress......")

res = encrypt(pt, k1, k2)

print("\nEntered Plain Text: ",pt)
print("Encryptred Text: ",res)