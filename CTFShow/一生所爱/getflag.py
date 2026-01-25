import numpy as np
import torchaudio as ta
from base64 import b64decode
import matplotlib.pyplot as plt
from Crypto.Util.number import long_to_bytes

hf = [i//2 for i in [1209, 1336, 1477, 1633]]
lf = [i // 2 for i in [697, 770, 852, 941]]
kb = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['E', '0', 'F', 'D']]
x = ta.load('flag.mp3')
datao = (x[0][0].numpy())
framerate = x[1]
df = int(framerate*0.15)
strflag = ''
for i in range(0,len(datao)-df,df):
    wave = datao[i+df//3: i+df]
    ffta =  np.abs(np.fft.fft(wave))
    lmax = ffta[lf]
    lindx = np.where(lmax==lmax.max())[0][0]
    hmax = ffta[hf]
    hindx = np.where(hmax==hmax.max())[0][0]
    strflag += kb[lindx][hindx]
    print(kb[lindx][hindx],end='')
    plt.clf()
    plt.plot(ffta[300:900])
    plt.pause(0.02)
flag = b64decode(long_to_bytes(int(strflag,16))).decode()
print(flag)
# ctfshow{A_simple_gift_to_allmy_friends_by_LoverlyFox}