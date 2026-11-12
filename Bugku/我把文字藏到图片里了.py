from PIL import Image
pic = Image.open('flag1.png')
a, b = pic.size
flag1 = ''
for y in range(b):
    for x in range(a):
        ff = pic.getpixel((x, y))
        flag1 += chr(ff)
print(flag1)
# flag{I_am_a_1ead_
from PIL import Image
pic = Image.open('flag2.png')
a, b = pic.size
flag2 = ''
for y in range(b):
    for x in range(a):
        ff = pic.getpixel((x, y))      
        if ff[2] == 0:
            flag2 += chr(ff[0])
print(flag2)
# i_1m_a_bod6_

# 维吉尼亚解密
# ciphertext = 'STM_BY_CQRV_DGHQHOKLT}'
# KEY = 'BYXS'
# alphabet = 'AHNBVDWZJILKGOQFMCUEYTXSPR'
flag3 = 'ctf_is_very_difficult}'
print(flag3)
flag = flag1 + flag2 + flag3
print(flag)
# flag{i_am_a_1ead_i_1m_a_bod6_ctf_is_very_difficult}