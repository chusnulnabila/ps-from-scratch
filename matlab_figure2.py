import numpy as np

def ybus(zdata):
    zdata = np.asarray(zdata, dtype=float)

    nl = zdata[:, 0].astype(int)   # bus asal
    nr = zdata[:, 1].astype(int)   # bus tujuan
    R  = zdata[:, 2]
    X  = zdata[:, 3]

    nbr  = len(nl)                          # jumlah saluran(branch)
    nbus = int(max(nl.max(), nr.max()))     # jumlah bus

    Z = R + 1j * X                          # impedansi saluran  
    y = 1.0 / Z                             # admitansi saluran

    Y = np.zeros((nbus, nbus), dtype=complex)

    # --- Pembentukan elemen off-diagonal ---
    for k in range(nbr):
        i = nl[k] - 1                       # konversi ke 0-based
        j = nr[k] - 1
        if nl[k] > 0 and nr[k] > 0:
            Y[i, j] -= y[k]
            Y[j, i] = Y[i, j]

    # --- Pembentukan elemen diagonal ---
    for n in range(nbus):
        for k in range(nbr):
            if (nl[k] - 1) == n or (nr[k] - 1) == n:
                Y[n, n] += y[k]

    return Y


# ==== GANTI BAGIAN INI DENGAN DATA SALURANMU ====
# zdata = [
#     [1, 2, 0, 2],
#     [1, 3, 0, 4],
#     [2, 3, 0, 5],
# ]
# ini data sesuai dengan yang ada di buku namun tidak memasukkan impedansi j1 dan j0.8 di dalam nya
zdata = [
    [1, 2, 0, 0.4],
    [1, 3, 0, 0.2],
    [2, 3, 0, 0.2],
    [3, 4, 0, 0.08],
]
# =================================================

Y = ybus(zdata)

np.set_printoptions(precision=4, suppress=True)
print("Matriks Y-bus:")
print(Y)