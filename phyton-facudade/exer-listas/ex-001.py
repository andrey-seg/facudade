# Programa para manipulação de vetor A com 6 números inteiros

# (a) Criando o vetor A com os valores especificados
A = [1, 0, 5, -2, -5, 7]
print("Vetor A criado:", A)
print()

# (b) Calculando a soma das posições A[0], A[1] e A[5]
soma = A[0] + A[1] + A[5]
print(f"Soma de A[0] + A[1] + A[5] = {A[0]} + {A[1]} + {A[5]} = {soma}")
print()

# (c) Modificando a posição 4 do vetor para o valor 100
print(f"Valor original em A[4]: {A[4]}")
A[4] = 100
print(f"Novo valor em A[4]: {A[4]}")
print()

# (d) Mostrando cada valor do vetor A, um em cada linha
print("Valores do vetor A (um por linha):")
for i in range(len(A)):
    print(f"A[{i}] = {A[i]}")