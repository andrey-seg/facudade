# Programa que manipula um vetor A com 6 números inteiros

# (a) Criando o vetor A com os valores especificados
A = [1, 0, 5, -2, -5, 7]

print("Vetor A criado com os valores:", A)
print()

# (b) Calculando a soma das posições A[0], A[1] e A[5]
soma = A[0] + A[1] + A[5]
print(f"Soma das posições A[0] + A[1] + A[5]: {A[0]} + {A[1]} + {A[5]} = {soma}")
print()

# (c) Modificando a posição 4 do vetor, atribuindo o valor 100
print(f"Valor original na posição 4: A[4] = {A[4]}")
A[4] = 100
print(f"Valor modificado na posição 4: A[4] = {A[4]}")
print()

# (d) Mostrando cada valor do vetor A, um em cada linha
print("Valores do vetor A (um por linha):")
for i in range(len(A)):
    print(f"A[{i}] = {A[i]}")