#📘 Exercício 4:
#Dada uma matriz 3x3, escreva um código que encontre o maior valor e diga a posição (linha e coluna) onde ele está.

matriz = [
    [30,50,100],
    [3,1000,00],
    [10,1001,0],
]

maior = matriz[0][0]
linha_maior = 0
coluna_maior = 0

for i in range (len(matriz)):
    for j in range (len(matriz[i])):
        if maior < matriz[i][j]:
            maior = matriz[i][j]
            linha_maior = i
            coluna_maior = j

print(f"O maior número é {maior} e está na posição [{linha_maior}][{coluna_maior}]")