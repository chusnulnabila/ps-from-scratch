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

# =========================================================
# Data sesuai Example 6.1 (Hadi Saadat)
# Kolom: [From, To, R, X]
# =========================================================
# zdata = [
#     [0, 1, 0, 1.0],
#     [0, 2, 0, 0.8],
#     [1, 2, 0, 0.4],
#     [1, 3, 0, 0.2],
#     [2, 3, 0, 0.2],
#     [3, 4, 0, 0.08],
# ]

Y = ybus(zdata)

np.set_printoptions(precision=4, suppress=True)
print("Matriks Y-bus:")
print(Y)

# --- Vektor arus bus (Ibus) ---
Ibus = np.array([-1j * 1.1, -1j * 1.25, 0, 0])
 
# --- Matriks impedansi bus (Zbus) = invers dari Ybus ---
Zbus = np.linalg.inv(Y)
print("\nMatriks Z-bus:")
print(Zbus)
 
# --- Tegangan bus (Vbus) = Zbus x Ibus ---
Vbus = Zbus @ Ibus
print("\nVektor tegangan bus (Vbus):")
print(Vbus)
 
print("\nDalam bentuk magnitude & sudut:")
for idx, v in enumerate(Vbus, start=1):
    print(f"  V{idx} = {abs(v):.4f} ∠ {np.degrees(np.angle(v)):.2f}°")