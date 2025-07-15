#Crie uma matriz 3x3 com valores inteiros fixos. Escreva um código que some todos os valores ímpares que estejam entre 10 e 50 (inclusive).

matriz= [
    [10,30,47],
    [13,44,50],
    [15,67,18]
]

soma=0

for i in range (len(matriz)):
    for j in range (len(matriz[i])):
        valor=matriz[i][j]

        if valor % 2 == 1 and 10<= valor <=50:
            soma+=valor
        

print(f"A soma de todos os numeros impares e de {soma}")

