valores = [1, 1, 1, 4, 5, 6, 7, 8, 1, 10]
repetidos = []

for i in range(len(valores)):
    cont = 0
    for j in range(len(valores)):
        if valores[i] == valores[j]:
            cont += 1
    if cont > 1 and valores[i] not in repetidos:
        repetidos.append(valores[i])
        print(f"O valor {valores[i]} se repete {cont} vezes")
