import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message
import pandas as pd

n = 174
d_v = 41
d_c = 58
snr = 20
H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
k = G.shape[1]
v = np.random.randint(2, size=k)
y = encode(G, v, snr)
d = decode(H, y, snr)
x = get_message(G, d)
print()


