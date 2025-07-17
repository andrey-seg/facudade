#Ler dois conjuntos de numeros reais, armazenando-os em vetores e calcular o produto ´
#escalar entre eles. Os conjuntos tem 5 elementos cada. Imprimir os dois conjuntos e o ˆ
#produto escalar, sendo que o produto escalar e dado por: ´ x1 ∗ y1 + x2 ∗ y2 + ... + xn ∗ yn.

v1=[]
v2=[]
v3=0

while len(v1)<2:
    num=int(input(f"Digite o numero {len(v1)+1} para o vetor 1: "))
    v1.append(num)


while len(v2)<2:
    num=int(input(f"Digite o numero {len(v2)+1} para o vetor 2: "))
    v2.append(num)

for i in range (2):
    v3+=v1[i]*v2[i]

print("valor de x1 & x2:")
print(v3)

    


