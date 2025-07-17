#21. Fac¸a um programa que receba do usuario dois vetores, ´ A e B, com 10 numeros inteiros ´
#cada. Crie um novo vetor denominado C calculando C = A - B. Mostre na tela os dados
#do vetor C.

v1=[]
v2=[]
c = []

while len(v1)<2:
    num1=int(input(f"numero {len(v1)+1}: "))

    v1.append(num1)

while len(v2)<2:
    num2=int(input(f"Numero {len(v2)+1}: "))

    v2.append(num2)

for i in range(0,len(v1)):
    for j in range(0,len(v1)):
        c.append(v1[i]-v2[i])
    

for i in range (10):
    print(f"c={[i]} = {c[i]}")




