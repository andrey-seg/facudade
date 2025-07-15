# Programa que lê números reais e calcula seus quadrados

# Vetores para armazenar os números originais e seus quadrados
numeros = []
quadrados = []

# Lendo 10 números reais
print("Digite 10 números reais:")
for i in range(10):
    numero = float(input(f"Digite o {i+1}º número: "))
    numeros.append(numero)

# Calculando o quadrado de cada número
for numero in numeros:
    quadrado = numero ** 2
    quadrados.append(quadrado)

print("\n" + "="*50)

# Imprimindo o conjunto original
print("CONJUNTO ORIGINAL:")
print("Posição |  Número")
print("-"*20)
for i in range(len(numeros)):
    print(f"   {i+1:2d}   | {numeros[i]:8.2f}")

print("\n" + "="*50)

# Imprimindo o conjunto dos quadrados
print("CONJUNTO DOS QUADRADOS:")
print("Posição | Quadrado")
print("-"*20)
for i in range(len(quadrados)):
    print(f"   {i+1:2d}   | {quadrados[i]:8.2f}")

print("\n" + "="*50)

# Imprimindo comparação lado a lado
print("COMPARAÇÃO:")
print("Posição | Original | Quadrado")
print("-"*35)
for i in range(len(numeros)):
    print(f"   {i+1:2d}   | {numeros[i]:8.2f} | {quadrados[i]:8.2f}")