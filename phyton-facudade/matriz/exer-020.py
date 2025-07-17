#0. Escreva um programa que leia numeros inteiros no intervalo [0,50] e os armazene em um ´
#vetor com 10 posic¸oes. Preencha um segundo vetor apenas com os n ˜ umeros ´ ´ımpares
#do primeiro vetor. Imprima os dois vetores, 2 elementos por linha.

vetor_a = []
vetor_b = []

print("Digite um numero entre 0 e 50")

while len(vetor_a)<10:
    num=int(input(f"Numero {len(vetor_a)+1}: "))

    if 0<= num <=50:
        vetor_a.append(num)
        if num % 2 ==0:
            vetor_b.append(num)

    else:
        print("valor fora do intervalo de numeros")

for i in range(0, len(vetor_a), 2):
    print(f"{vetor_a[i]:<5}", end=" ")
    if i+1 < len(vetor_a):
        print(f"{vetor_a[i+1]:<5}")
    else:
        print()

print("\nVetor B (valores ímpares):")
for i in range(0, len(vetor_b), 2):
    print(f"{vetor_b[i]:<5}", end=" ")
    if i+1 < len(vetor_b):
        print(f"{vetor_b[i+1]:<5}")
    else:
        print()
