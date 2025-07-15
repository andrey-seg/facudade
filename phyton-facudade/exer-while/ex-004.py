import math
import time
import os

A = 0
B = 0

while True:
    z = [0] * 1760
    b = [' '] * 1760

    for j in range(0, 628, 7):  # 0 to 2pi, step ~0.07
        for i in range(0, 628, 2):  # 0 to 2pi, step ~0.02
            j_ = j / 100.0
            i_ = i / 100.0

            c = math.sin(i_)
            d = math.cos(j_)
            e = math.sin(A)
            f = math.sin(j_)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i_)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e

            x = int(30 + 20 * D * (l * h * m - t * n))
            y = int(10 + 10 * D * (l * h * n + t * m))
            o = x + 80 * y
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))

            if 0 <= y < 22 and 0 <= x < 80 and D > z[o]:
                z[o] = D
                b[o] = ".,-~:;=!*#$@"[N if N > 0 else 0]

    # Limpar a tela e posicionar o cursor
    os.system('clear')  # use 'cls' no Windows
    print(''.join([b[i] if i % 80 else '\n' for i in range(1760)]))

    A += 0.04
    B += 0.08
    time.sleep(0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
