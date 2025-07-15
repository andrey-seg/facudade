#Escreva um programa que percorra uma matriz 4x4 e some todos os valores pares que estão na diagonal principal.

matriz= [
    [10,20,30,40],
    [28,3,14,101],
    [102,38,0,18],
    [30,33,77,90]
]

soma=0

for i in range (len(matriz)):
    valor = matriz[i][i]

    if valor % 2 == 0:
        soma+=valor

print(f"A soma dos valores pares da diagonal sao {soma}")