# Programa que lê um vetor de 8 posições e soma valores de posições X e Y

# Criando o vetor
vetor = []

# Lendo os 8 valores do vetor
print("Digite 8 valores para o vetor:")
for i in range(8):
    valor = float(input(f"Digite o valor para a posição {i}: "))
    vetor.append(valor)

print("\nVetor criado:")
for i in range(len(vetor)):
    print(f"Posição {i}: {vetor[i]}")

print("\n" + "="*40)

# Lendo as posições X e Y
print("Agora digite duas posições do vetor (0 a 7):")

# Validação da posição X
while True:
    try:
        X = int(input("Digite a posição X (0-7): "))
        if 0 <= X <= 7:
            break
        else:
            print("Erro: A posição deve estar entre 0 e 7!")
    except ValueError:
        print("Erro: Digite um número inteiro válido!")

# Validação da posição Y
while True:
    try:
        Y = int(input("Digite a posição Y (0-7): "))
        if 0 <= Y <= 7:
            break
        else:
            print("Erro: A posição deve estar entre 0 e 7!")
    except ValueError:
        print("Erro: Digite um número inteiro válido!")

print("\n" + "="*40)

# Calculando e exibindo a soma
valor_X = vetor[X]
valor_Y = vetor[Y]
soma = valor_X + valor_Y

print("RESULTADO:")
print(f"Valor na posição {X}: {valor_X}")
print(f"Valor na posição {Y}: {valor_Y}")
print(f"Soma dos valores: {valor_X} + {valor_Y} = {soma}")