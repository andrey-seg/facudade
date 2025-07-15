#Q2

temperaturas=[
    [18,22,41],
    [36,39,20],
    [19,25,40]
]

soma=0

for i in range (len(temperaturas)):
    for j in range (len(temperaturas[i])):

        Valor=temperaturas[i][j]

        if Valor % 2 == 0 and 20 <= Valor <= 40:
            soma+=Valor

print(f"A soma dos valores e igual a {soma}")

