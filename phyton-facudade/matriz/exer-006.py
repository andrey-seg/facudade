#Fac¸a um programa que receba do usuario um vetor com 10 posic¸ ´ oes. Em seguida dever ˜ a´
#ser impresso o maior e o menor elemento do vetor

vetor = [10, 2, 7, 10, 7, 6, 16, 8, 9, 3]

maior = vetor[0]
menor = vetor[0]

for num in (vetor):
    if num > maior:
        maior=num

    elif menor > num:
        menor=num

print(f"O maior numero e {maior}")
print(f"O menor numero e {menor}")