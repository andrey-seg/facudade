#📘 Exercício 5:
#Dada uma matriz qualquer, escreva um código que conte quantos números múltiplos de 5 existem nela.

matriz=[
    [5,30,70],
    [21,10,40],
    [50,33,00]
]

soma=0

for i in range (len(matriz)):
    for j in range (len(matriz)):
        valor=matriz[i][j]

        if valor % 5 ==0:
            soma+=1

print(f"Existem {soma} numeros que sao multiplos de 5")
