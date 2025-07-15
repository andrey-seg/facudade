m1=[[1,2], [14,10]]
m2=[[2,3], [-10,-5]]

soma = [[0, 0], [0, 0]]
sub = [[0, 0], [0, 0]]

print("=+="*20)
print("menu")

print("1- Soma as matrizes")
print("2- subtrai as matrizes")
print("3- imprime as matrizes")
print("0- encerrar o programa")

operador=int(input("Operador: "))

print("=+="*20)

def mais (m1, m2):
    for i in range (2):
        for j in range (2):
            soma[i][j]= m1[i][j]+m2[i][j]

    print(f"A soma das duas matrizes e igual a:")
    for linha in soma:
        print(linha)


def menos (m1,m2):
    for i in range (2):
        for j in range (2):
            sub[i][j]=m1[i][j]-m2[i][j]

    print("O resultado da subtracao das duas matrizes e igual a:")
    for linha in sub:
        print(linha)


def imprimir (m1,m2):

    print("matrizes impresas: ")

    for linha in m1: 
        print(linha)

    for linha in m2:
        print(linha)
        

if operador == 1:
    mais(m1,m2)

elif operador == 2:
    menos(m1,m2)

elif operador == 3:
    imprimir(m1,m2)

elif operador == 0:
    print("sistema encerrado")

else:
    print("opcao invalida")
    