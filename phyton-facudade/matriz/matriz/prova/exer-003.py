temperaturas = [
    [28, 36, 41],
    [30, 32, 38],
    [27, 35, 42]
]

soma=0

for i in range (len(temperaturas)):
    for j in range (len(temperaturas[i])):
        valor=temperaturas[i][j]

        if valor > 35:
            soma+=1

print(f"A quantidade de valores  acima de 35 graus e de {soma}")