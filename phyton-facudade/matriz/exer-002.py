# Programa que lê 6 valores inteiros e os exibe na tela

# Lista para armazenar os valores
valores = []

# Lendo os 6 valores inteiros
print("Digite 6 valores inteiros:")
for i in range(6):
    valor = int(input(f"Digite o {i+1}º valor: "))
    valores.append(valor)

print()  # Linha em branco para separar

# Exibindo os valores lidos
print("Os valores lidos foram:")
for i in range(len(valores)):
    print(f"Valor {i+1}: {valores[i]}")