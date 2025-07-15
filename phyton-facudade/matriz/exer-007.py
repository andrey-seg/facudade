#Escreva um programa que leia 10 numeros inteiros e os armazene em um vetor. Imprima ´
#o vetor, o maior elemento e a posic¸ao que ele se encontra.

vetor = [10, 2, 7, 10, 7, 6, 16, 8, 9, 3]

maior = vetor[0]
posicao = 0

for i in range (1, 10):
    if vetor[i] > maior:
        maior = vetor[i]
        posicao = i


print(f"O maior numero e {maior} e esta na pocicao {posicao}")