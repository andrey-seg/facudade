#Fac¸a um programa que leia dois vetores de 10 posic¸oes e calcule outro vetor contendo, ˜
#nas posic¸oes pares os valores do primeiro e nas posic¸ ˜ oes impares os valores do se- ˜
#gundo.

v1=[]
v2=[]
v3=[]

while len(v1)<2:
    num=int(input(f"Digite o numero {len(v1)+1}: "))
    v1.append(num)

while len(v2)<2:
    num=int(input(f"Digite o numero {len(v2)+1}: "))
    v2.append(num)



for i in range (2):

    if v2[i] % 2 !=0:
        v3.append(v1[i])

    if v1[i] % 2 ==0:
        v3.append(v1[i])


print(v3)