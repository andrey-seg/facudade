#Leia um vetor de 10 posic¸oes e atribua valor 0 para todos os elementos que possu ˜ ´ırem
#valores negativos.

valor=[]

for i in range(10):
    numero = float(input(f"digite o valor da posiccao {i+1}: "))
    if numero < 0:
        valor.append(0)
    else:
        valor.append(numero)

print(valor)