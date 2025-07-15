#1. Fac¸a um programa que preencha um vetor com 10 numeros reais, calcule e mostre a ´
#quantidade de numeros negativos e a soma dos n ´ umeros positivos desse vetor. 

vetor=[]
neg=0
positivo=0

for i in range (10):
    numeros=int(input(f"Digite um o {i+1} numero: "))
    vetor.append(numeros)

for num in (vetor):
    if num < 0:
        neg+=1

    else:
        positivo+=num

print(f"Temos {neg} numeros negativos e a soma dos positivos e igual a {positivo}")
