import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message
import pandas as pd


all_data = []
for d_v in range(2, 83):
    for d_c in [3, 6, 29, 58, 87, 174]:
        if d_c > d_v:
            row_data = {'d_v': d_v, 'd_c': d_c}
            n = 174
            # d_v = 5
            # d_c = 6
            snr = 20
            H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
            k = G.shape[1]
            row_data['k'] = k
            # v = np.random.randint(2, size=k)
            # y = encode(G, v, snr)
            # d = decode(H, y, snr)
            # x = get_message(G, d)
            all_data.append(row_data)
            df = pd.DataFrame(all_data)
            df.to_csv("C:/Users/edmu2/OneDrive/Desktop/data.csv")


