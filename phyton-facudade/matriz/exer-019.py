#. Fac¸a um vetor de tamanho 50 preenchido com o seguinte valor: (i+ 5 ∗ i)%(i+ 1), sendo
#i a posic¸ao do elemento no vetor. Em seguida imprima o vetor na tela. 

vetor=[]



for i in range (50):
    valor= (1+ 5* i)%(i+ 1)

    vetor.append(valor)

print("Resultado da operacao: ")
print(vetor)

    