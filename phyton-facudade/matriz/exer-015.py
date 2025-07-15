#Leia um vetor com 20 numeros inteiros. Escreva os elementos do vetor eliminando ele- ´
#mentos repetidos.
valores=[1, 2, 3, 10, 494, 10, 9, 90, 10, 19, 33, 79, 13, 18, 19, 20, 29, 18, 10, 10]
sem_rep=[]

for i in range(len(valores)):
    if valores[i] not in sem_rep:
        sem_rep.append(valores[i])

print("Valores sem repetição:")
print(sem_rep)

